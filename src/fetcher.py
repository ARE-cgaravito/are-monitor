"""
ARE Monitor — Fetcher Module v8
Fixed: SECOP Integrado endpoint, SSL errors, URL corrections, JSON safety
"""

import feedparser
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import pytz
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
COLOMBIA_TZ = pytz.timezone("America/Bogota")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ARE-Monitor/1.0; +https://github.com/ARE-cgaravito/are-monitor)"
}


def fetch_source(source: dict, since_hours: int = 96) -> list:
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
            logger.warning(f"Unknown fetch method '{method}' for {source['id']}")
            return []
    except Exception as e:
        logger.error(f"Failed to fetch {source['id']}: {e}")
        return []


# ─── RSS ──────────────────────────────────────────────────────────────────────

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
            "title": _safe(entry.get("title", "")),
            "url": entry.get("link", ""),
            "source": source["name"],
            "source_id": source["id"],
            "category": source["category"],
            "subcategory": source["subcategory"],
            "published": pub.isoformat() if pub else None,
            "raw_text": _clean(entry.get("summary", "") + " " + entry.get("title", "")),
        })
    logger.info(f"  → {len(results)} items from {source['id']}")
    return results


# ─── SCRAPER ──────────────────────────────────────────────────────────────────

def _fetch_scrape(source: dict) -> list:
    cfg = source.get("scrape_config", {})
    url = source["url"]
    verify_ssl = source.get("verify_ssl", True)
    logger.info(f"Scraping: {url}")

    try:
        resp = requests.get(url, headers=HEADERS, timeout=20, verify=verify_ssl)
        resp.raise_for_status()
    except requests.exceptions.SSLError:
        logger.warning(f"SSL error for {url}, retrying without verification")
        resp = requests.get(url, headers=HEADERS, timeout=20, verify=False)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    listing_sel = cfg.get("listing_selector", "article")
    title_sel   = cfg.get("title_selector", "h2")
    link_sel    = cfg.get("link_selector", "a")
    date_sel    = cfg.get("date_selector", "time")

    items = soup.select(listing_sel)
    results = []
    for item in items[:40]:
        title_el = item.select_one(title_sel)
        link_el  = item.select_one(link_sel)
        date_el  = item.select_one(date_sel)

        title    = title_el.get_text(strip=True) if title_el else ""
        href     = link_el.get("href", "") if link_el else ""
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
            "title": _safe(title),
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


# ─── API DISPATCHER ───────────────────────────────────────────────────────────

def _fetch_api(source: dict, since: datetime) -> list:
    api_type = source["api_config"]["type"]
    dispatch = {
        "ted":              _fetch_ted,
        "secop_integrado":  _fetch_secop_integrado,
        "contracts_finder": _fetch_contracts_finder,
        "chilecompra":      _fetch_chilecompra,
    }
    fn = dispatch.get(api_type)
    if fn:
        return fn(source, since)
    logger.warning(f"No handler for API type '{api_type}'")
    return []


# ─── TED (EU) ─────────────────────────────────────────────────────────────────

def _fetch_ted(source: dict, since: datetime) -> list:
    cfg = source["api_config"]
    cpv_codes = cfg.get("cpv_codes", [])
    results = []
    for cpv in cpv_codes:
        try:
            url = "https://ted.europa.eu/api/v3.0/notices/search"
            payload = {
                "query": f"cpv:{cpv}",
                "fields": ["title", "noticeNumber", "publicationDate",
                           "deadlineDate", "buyerName", "estimatedValue",
                           "currency", "procedureType"],
                "page": 1, "pageSize": 20,
                "sortField": "publicationDate", "sortOrder": "desc",
                "scope": "ACTIVE",
            }
            resp = requests.post(url, json=payload, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                logger.warning(f"TED API returned {resp.status_code} for CPV {cpv}")
                continue
            data = resp.json()
            for notice in data.get("notices", []):
                pub = _parse_date(notice.get("publicationDate"))
                if pub and pub < since:
                    continue
                title = notice.get("title", "")
                if isinstance(title, dict):
                    title = title.get("text", "") or next(iter(title.values()), "")
                results.append({
                    "id": notice.get("noticeNumber", ""),
                    "title": _safe(str(title)),
                    "url": f"https://ted.europa.eu/en/notice/{notice.get('noticeNumber', '')}",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": pub.isoformat() if pub else None,
                    "deadline": notice.get("deadlineDate"),
                    "budget": f"{notice.get('estimatedValue', '')} {notice.get('currency', '')}".strip(),
                    "organizer": _safe(str(notice.get("buyerName", ""))),
                    "raw_text": _safe(str(title)),
                })
        except Exception as e:
            logger.error(f"TED fetch error for CPV {cpv}: {e}")
    logger.info(f"  → {len(results)} items from TED")
    return results


# ─── SECOP INTEGRADO ──────────────────────────────────────────────────────────

def _fetch_secop_integrado(source: dict, since: datetime) -> list:
    """
    Uses the SECOP Integrado dataset which combines SECOP I + II.
    Dataset ID: rpmr-utcd on datos.gov.co
    Uses simple $q full-text search (no special characters in $where).
    """
    cfg      = source["api_config"]
    endpoint = cfg["endpoint"]
    keywords = cfg.get("keywords", [])
    results  = []

    for keyword in keywords:
        try:
            params = {
                "$q": keyword,
                "$limit": 50,
                "$order": ":id",
            }
            resp = requests.get(
                endpoint, params=params,
                headers=HEADERS, timeout=30
            )
            if resp.status_code != 200:
                logger.warning(
                    f"SECOP Integrado returned {resp.status_code} "
                    f"for '{keyword}': {resp.text[:150]}"
                )
                continue

            data = resp.json()
            for item in data:
                # Official SECOP process number — try all known field names
                process_number = (
                    item.get("proceso_de_compra")
                    or item.get("numero_del_proceso")
                    or item.get("id_proceso")
                    or item.get("referencia_proceso")
                    or item.get("numero_proceso")
                    or ""
                )
                title = (item.get("descripcion_del_proceso")
                         or item.get("objeto_del_proceso")
                         or item.get("nombre_del_proceso", ""))
                if not title:
                    continue

                uid = f"secop_{process_number or title[:40]}"
                if process_number:
                    direct_url = f"https://www.contratos.gov.co/consultas/inicioConsulta.do?busqueda={process_number}"
                else:
                    direct_url = item.get("url_proceso") or "https://www.contratos.gov.co"

                results.append({
                    "id": uid,
                    "title": _safe(title),
                    "url": direct_url,
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": item.get("fecha_de_publicacion_del_proceso"),
                    "deadline": item.get("fecha_limite_de_recepcion_de_propuestas"),
                    "budget": _safe(str(
                        item.get("cuantia_proceso")
                        or item.get("valor_del_contrato", "")
                    )),
                    "organizer": _safe(item.get("nombre_entidad", "")),
                    "city": item.get("municipio", ""),
                    "department": item.get("departamento", ""),
                    "modality": item.get("modalidad_de_contratacion", ""),
                    "process_number": _safe(process_number),
                    "raw_text": _safe(
                        f"{title} {item.get('nombre_entidad', '')} "
                        f"{item.get('municipio', '')} {process_number}"
                    ),
                })
        except Exception as e:
            logger.error(f"SECOP Integrado error for '{keyword}': {e}")

    # Deduplicate
    seen, unique = set(), []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)

    logger.info(f"  → {len(unique)} items from SECOP Integrado")
    return unique


# ─── CONTRACTS FINDER (UK) ────────────────────────────────────────────────────

def _fetch_contracts_finder(source: dict, since: datetime) -> list:
    cfg = source["api_config"]
    results = []
    for keyword in cfg.get("keywords", []):
        try:
            url    = "https://www.contractsfinder.service.gov.uk/Published/Notices/PublishedNoticesSearchV2"
            params = {"keyword": keyword, "size": 25}
            resp   = requests.get(url, params=params, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                continue
            data = resp.json()
            for notice in data.get("results", []):
                results.append({
                    "id": notice.get("id", ""),
                    "title": _safe(notice.get("title", "")),
                    "url": notice.get("link", "https://www.contractsfinder.service.gov.uk"),
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": notice.get("publishedAt"),
                    "deadline": notice.get("deadlineUtc"),
                    "budget": _safe(str(notice.get("value", ""))),
                    "organizer": _safe(notice.get("organisationName", "")),
                    "raw_text": _safe(
                        f"{notice.get('title', '')} {notice.get('description', '')}"
                    ),
                })
        except Exception as e:
            logger.error(f"Contracts Finder error for '{keyword}': {e}")
    logger.info(f"  → {len(results)} items from Contracts Finder")
    return results


# ─── CHILECOMPRA ──────────────────────────────────────────────────────────────

def _fetch_chilecompra(source: dict, since: datetime) -> list:
    cfg = source["api_config"]
    results = []
    for keyword in cfg.get("keywords", []):
        try:
            url    = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
            params = {"busqueda": keyword, "estado": "publicada"}
            resp   = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            for item in resp.json().get("Listado", []):
                results.append({
                    "id": item.get("CodigoExterno", ""),
                    "title": _safe(item.get("Nombre", "")),
                    "url": f"https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs={item.get('CodigoExterno', '')}",
                    "source": source["name"],
                    "source_id": source["id"],
                    "category": source["category"],
                    "subcategory": source["subcategory"],
                    "published": item.get("FechaPublicacion"),
                    "deadline": item.get("FechaCierre"),
                    "budget": _safe(str(item.get("MontoEstimado", ""))),
                    "organizer": _safe(item.get("Nombre", "")),
                    "raw_text": _safe(f"{item.get('Nombre', '')} {item.get('Descripcion', '')}"),
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
    import re
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return _safe(text.strip()[:2000])


def _safe(text: str) -> str:
    """Remove control characters that break JSON serialisation."""
    import re
    if not text:
        return ""
    # Strip control chars (except normal whitespace)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(text))
    return text.strip()
