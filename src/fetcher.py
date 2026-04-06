"""
ARE Monitor — Fetcher Module
Handles RSS feeds, web scraping, and public API sources.
"""

import feedparser
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import pytz

logger = logging.getLogger(__name__)
COLOMBIA_TZ = pytz.timezone("America/Bogota")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ARE-Monitor/1.0; +https://github.com/ARE-cgaravito/are-monitor)"
}


def fetch_source(source: dict, since_hours: int = 96) -> list:
    """
    Main dispatcher. Returns a list of raw opportunity dicts from a source.
    since_hours: only return items published in the last N hours (default 96 = 4 days).
    """
    method = source.get("fetch_method")
    since = datetime.now(tz=pytz.utc) - timedelta(hours=since_hours)

    try:
        if method == "rss":
            return _fetch_rss(source, since)
        elif method == "scrape":
            return _fetch_scrape(source)
        elif method == "api":
            return _fetch_api(source, since)
        else:
            logger.warning(f"Unknown fetch method '{method}' for source {source['id']}")
            return []
    except Exception as e:
        logger.error(f"Failed to fetch {source['id']}: {e}")
        return []


# ─── RSS ─────────────────────────────────────────────────────────────────────

def _fetch_rss(source: dict, since: datetime) -> list:
    rss_url = source.get("rss") or source.get("url")
    logger.info(f"Fetching RSS: {rss_url}")
    feed = feedparser.parse(rss_url)
    results = []
    for entry in feed.entries:
        pub = _parse_date(entry.get("published") or entry.get("updated"))
        if pub and pub < since:
            continue
        results.append({
            "id": entry.get("id") or entry.get("link"),
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "source": source["name"],
            "source_id": source["id"],
            "category": source["category"],
            "subcategory": source["subcategory"],
            "published": pub.isoformat() if pub else None,
            "summary": _clean(entry.get("summary", "")),
            "raw_text": _clean(entry.get("summary", "") + " " + entry.get("title", "")),
        })
    logger.info(f"  → {len(results)} items from {source['id']}")
    return results


# ─── WEB SCRAPER ─────────────────────────────────────────────────────────────

def _fetch_scrape(source: dict) -> list:
    cfg = source.get("scrape_config", {})
    url = source["url"]
    logger.info(f"Scraping: {url}")

    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    listing_sel = cfg.get("listing_selector", "article")
    title_sel = cfg.get("title_selector", "h2")
    link_sel = cfg.get("link_selector", "a")
    date_sel = cfg.get("date_selector", "time")

    items = soup.select(listing_sel)
    results = []

    for item in items[:40]:  # cap at 40 items per scrape
        title_el = item.select_one(title_sel)
        link_el = item.select_one(link_sel)
        date_el = item.select_one(date_sel)

        title = title_el.get_text(strip=True) if title_el else ""
        href = link_el.get("href", "") if link_el else ""
        if href and not href.startswith("http"):
            from urllib.parse import urljoin
            href = urljoin(url, href)
        date_str = date_el.get_text(strip=True) if date_el else ""
        if date_el and date_el.get("datetime"):
            date_str = date_el["datetime"]

        if not title or not href:
            continue

        results.append({
            "id": href,
            "title": title,
            "url": href,
            "source": source["name"],
            "source_id": source["id"],
            "category": source["category"],
            "subcategory": source["subcategory"],
            "published": date_str,
            "raw_text": _clean(item.get_text(separator=" ", strip=True)),
        })

    logger.info(f"  → {len(results)} items from {source['id']}")
    return results


# ─── API FETCHERS ─────────────────────────────────────────────────────────────

def _fetch_api(source: dict, since: datetime) -> list:
    api_type = source["api_config"]["type"]
    if api_type == "ted":
        return _fetch_ted(source, since)
    elif api_type == "secop1":
        return _fetch_secop1(source, since)
    elif api_type == "secop2":
        return _fetch_secop2(source, since)
    elif api_type == "contracts_finder":
        return _fetch_contracts_finder(source, since)
    elif api_type == "sam":
        return _fetch_sam(source, since)
    elif api_type == "chilecompra":
        return _fetch_chilecompra(source, since)
    else:
        logger.warning(f"No handler for API type '{api_type}'")
        return []


def _fetch_ted(source: dict, since: datetime) -> list:
    """TED (EU) – uses their open search API"""
    cfg = source["api_config"]
    cpv_codes = cfg.get("cpv_codes", [])
    results = []

    for cpv in cpv_codes:
        try:
            # TED public search API
            url = "https://ted.europa.eu/api/v3.0/notices/search"
            params = {
                "q": f"cpv:{cpv}",
                "fields": "title,noticeNumber,publicationDate,deadlineDate,buyerName,estimatedValue,currency,cpvCodes,procedureType",
                "page": 1,
                "pageSize": 25,
                "sortField": "publicationDate",
                "sortOrder": "desc",
            }
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                logger.warning(f"TED API returned {resp.status_code} for CPV {cpv}")
                continue
            data = resp.json()
            for notice in data.get("notices", []):
                pub = _parse_date(notice.get("publicationDate"))
                if pub and pub < since:
                    continue
                results.append({
                    "id": notice.get("noticeNumber", ""),
                    "title": notice.get("title", {}).get("text", ""),
                    "url": f"https://ted.europa.eu/udl?uri=TED:NOTICE:{notice.get('noticeNumber', '')}:TEXT:EN:HTML",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": pub.isoformat() if pub else None,
                    "deadline": notice.get("deadlineDate"),
                    "budget": f"{notice.get('estimatedValue')} {notice.get('currency', '')}".strip(),
                    "organizer": notice.get("buyerName", ""),
                    "cpv_codes": ", ".join(notice.get("cpvCodes", [])),
                    "raw_text": notice.get("title", {}).get("text", ""),
                })
        except Exception as e:
            logger.error(f"TED fetch error for CPV {cpv}: {e}")

    logger.info(f"  → {len(results)} items from TED")
    return results


def _fetch_secop1(source: dict, since: datetime) -> list:
    """SECOP I via datos.gov.co open data API (Socrata)"""
    cfg = source["api_config"]
    endpoint = cfg["endpoint"]
    keywords = cfg.get("keywords", [])
    results = []

    since_str = since.strftime("%Y-%m-%dT%H:%M:%S")

    for keyword in keywords:
        try:
            params = {
                "$where": f"descripcion_del_proceso like '%{keyword}%' AND fecha_de_publicacion_del_proceso >= '{since_str}'",
                "$order": "fecha_de_publicacion_del_proceso DESC",
                "$limit": 50,
            }
            resp = requests.get(endpoint, params=params, headers=HEADERS, timeout=30)
            if resp.status_code != 200:
                logger.warning(f"SECOP I API returned {resp.status_code}")
                continue
            data = resp.json()
            for item in data:
                process_id = item.get("id_del_proceso") or item.get("numero_de_proceso", "")
                title = item.get("descripcion_del_proceso", item.get("objeto_del_proceso", ""))
                if not title:
                    continue
                results.append({
                    "id": f"secop1_{process_id}",
                    "title": title,
                    "url": item.get("url_proceso", f"https://www.contratos.gov.co/consultas/inicioConsulta.do"),
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": item.get("fecha_de_publicacion_del_proceso"),
                    "deadline": item.get("fecha_limite_de_recepcion_de_propuestas"),
                    "budget": item.get("cuantia_proceso") or item.get("valor_del_contrato"),
                    "organizer": item.get("nombre_entidad", ""),
                    "city": item.get("municipio", ""),
                    "department": item.get("departamento", ""),
                    "modality": item.get("modalidad_de_contratacion", ""),
                    "raw_text": f"{title} {item.get('objeto_del_proceso', '')} {item.get('nombre_entidad', '')}",
                })
        except Exception as e:
            logger.error(f"SECOP I fetch error for keyword '{keyword}': {e}")

    # Deduplicate by id
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)

    logger.info(f"  → {len(unique)} items from SECOP I")
    return unique


def _fetch_secop2(source: dict, since: datetime) -> list:
    """SECOP II via datos.gov.co open data API"""
    cfg = source["api_config"]
    endpoint = cfg["endpoint"]
    keywords = cfg.get("keywords", [])
    results = []

    since_str = since.strftime("%Y-%m-%dT%H:%M:%S")

    for keyword in keywords:
        try:
            params = {
                "$where": f"descripcion_del_proceso like '%{keyword}%' AND fecha_de_publicacion_del_proceso >= '{since_str}'",
                "$order": "fecha_de_publicacion_del_proceso DESC",
                "$limit": 50,
            }
            resp = requests.get(endpoint, params=params, headers=HEADERS, timeout=30)
            if resp.status_code != 200:
                logger.warning(f"SECOP II API returned {resp.status_code}")
                continue
            data = resp.json()
            for item in data:
                process_id = item.get("id_del_proceso") or item.get("referencia", "")
                title = item.get("descripcion_del_proceso", item.get("nombre_del_procedimiento", ""))
                if not title:
                    continue
                results.append({
                    "id": f"secop2_{process_id}",
                    "title": title,
                    "url": f"https://www.colombiacompra.gov.co/secop-ii",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": item.get("fecha_de_publicacion_del_proceso"),
                    "deadline": item.get("fecha_limite_de_recepcion_de_propuestas"),
                    "budget": item.get("presupuesto_oficial") or item.get("cuantia_proceso"),
                    "organizer": item.get("nombre_entidad", ""),
                    "city": item.get("ciudad", ""),
                    "department": item.get("departamento", ""),
                    "modality": item.get("modalidad_de_contratacion", ""),
                    "raw_text": f"{title} {item.get('nombre_entidad', '')}",
                })
        except Exception as e:
            logger.error(f"SECOP II fetch error for keyword '{keyword}': {e}")

    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)

    logger.info(f"  → {len(unique)} items from SECOP II")
    return unique


def _fetch_contracts_finder(source: dict, since: datetime) -> list:
    """UK Contracts Finder API"""
    cfg = source["api_config"]
    keywords = cfg.get("keywords", [])
    results = []
    since_str = since.strftime("%Y-%m-%dT%H:%M:%SZ")

    for keyword in keywords:
        try:
            url = "https://www.contractsfinder.service.gov.uk/Published/Notices/PublishedNoticesSearchV2"
            params = {
                "publishedFrom": since_str,
                "keyword": keyword,
                "size": 25,
            }
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for notice in data.get("results", data.get("notices", [])):
                results.append({
                    "id": notice.get("id", notice.get("noticeIdentifier", "")),
                    "title": notice.get("title", ""),
                    "url": notice.get("links", {}).get("notices", [{}])[0].get("url", "https://www.contractsfinder.service.gov.uk"),
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": notice.get("publishedAt"),
                    "deadline": notice.get("tenderingProcess", {}).get("tenderPeriod", {}).get("endDate"),
                    "budget": str(notice.get("tender", {}).get("value", {}).get("amount", "")),
                    "organizer": notice.get("buyer", {}).get("name", ""),
                    "raw_text": f"{notice.get('title', '')} {notice.get('description', '')}",
                })
        except Exception as e:
            logger.error(f"Contracts Finder error for '{keyword}': {e}")

    logger.info(f"  → {len(results)} items from Contracts Finder")
    return results


def _fetch_sam(source: dict, since: datetime) -> list:
    """SAM.gov – US federal procurement (public API)"""
    cfg = source["api_config"]
    keywords = cfg.get("keywords", [])
    results = []
    since_str = since.strftime("%m/%d/%Y")

    for keyword in keywords:
        try:
            url = "https://api.sam.gov/opportunities/v2/search"
            params = {
                "q": keyword,
                "postedFrom": since_str,
                "limit": 25,
                "offset": 0,
            }
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                logger.warning(f"SAM.gov returned {resp.status_code}")
                continue
            data = resp.json()
            for opp in data.get("opportunitiesData", []):
                results.append({
                    "id": opp.get("noticeId", ""),
                    "title": opp.get("title", ""),
                    "url": f"https://sam.gov/opp/{opp.get('noticeId', '')}/view",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": opp.get("postedDate"),
                    "deadline": opp.get("responseDeadLine"),
                    "budget": None,
                    "organizer": opp.get("fullParentPathName", ""),
                    "raw_text": f"{opp.get('title', '')} {opp.get('description', '')}",
                })
        except Exception as e:
            logger.error(f"SAM.gov error for '{keyword}': {e}")

    logger.info(f"  → {len(results)} items from SAM.gov")
    return results


def _fetch_chilecompra(source: dict, since: datetime) -> list:
    """ChileCompra – public API (no auth required for basic search)"""
    cfg = source["api_config"]
    keywords = cfg.get("keywords", [])
    results = []

    for keyword in keywords:
        try:
            url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
            params = {
                "busqueda": keyword,
                "estado": "publicada",
            }
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for item in data.get("Listado", []):
                results.append({
                    "id": item.get("CodigoExterno", ""),
                    "title": item.get("Nombre", ""),
                    "url": f"https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs={item.get('CodigoExterno', '')}",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": item.get("FechaPublicacion"),
                    "deadline": item.get("FechaCierre"),
                    "budget": str(item.get("MontoEstimado", "")),
                    "organizer": item.get("Nombre", ""),
                    "raw_text": f"{item.get('Nombre', '')} {item.get('Descripcion', '')}",
                })
        except Exception as e:
            logger.error(f"ChileCompra error for '{keyword}': {e}")

    logger.info(f"  → {len(results)} items from ChileCompra")
    return results


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _parse_date(date_str) -> datetime | None:
    if not date_str:
        return None
    try:
        dt = dateparser.parse(str(date_str))
        if dt and dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        return dt
    except Exception:
        return None


def _clean(text: str) -> str:
    """Basic text cleanup."""
    import re
    text = re.sub(r"<[^>]+>", " ", text)   # strip HTML tags
    text = re.sub(r"\s+", " ", text)         # collapse whitespace
    return text.strip()[:2000]               # cap at 2000 chars
