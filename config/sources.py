# ARE Monitor — Source Configuration
# Each source has: name, url, category, subcategory, fetch_method, and optional extras

SOURCES = [

    # ─── INTERNATIONAL ARCHITECTURE & DESIGN COMPETITIONS ───────────────────

    {
        "id": "bustler",
        "name": "Bustler",
        "url": "https://bustler.net/competitions",
        "rss": "https://bustler.net/rss/competitions",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "archdaily_competitions",
        "name": "ArchDaily – Competitions",
        "url": "https://www.archdaily.com/search/competitions",
        "rss": "https://www.archdaily.com/search/competitions/feed",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article.afd-item, div.search-result",
            "title_selector": "h3, h2",
            "link_selector": "a",
            "date_selector": "time",
        },
    },
    {
        "id": "competitions_archi",
        "name": "Competitions.Archi",
        "url": "https://competitions.archi",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition-item, .card",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": ".date, time",
        },
    },
    {
        "id": "world_architecture",
        "name": "World Architecture Competitions",
        "url": "https://worldarchitecture.org/competitions",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "div.compWrap, article, .competition",
            "title_selector": "h2, h3, .compTitle",
            "link_selector": "a",
            "date_selector": ".date, .deadline",
        },
    },
    {
        "id": "uia",
        "name": "UIA – International Union of Architects",
        "url": "https://www.uia-architectes.org/en/competitions/",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition-item, li.views-row",
            "title_selector": "h2, h3, .views-field-title",
            "link_selector": "a",
            "date_selector": ".date-display-single, .field-name-field-date",
        },
    },

    # ─── INTERNATIONAL TENDERS ───────────────────────────────────────────────

    {
        "id": "ted",
        "name": "TED – Tenders Electronic Daily",
        "url": "https://ted.europa.eu/api/v3.0/notices/search",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "ted",
            "cpv_codes": ["71220000", "71221000", "71240000", "71310000", "71400000", "71410000"],
            "fields": "title,noticeNumber,publicationDate,deadlineDate,buyerName,buyerCountry,estimatedValue,currency,cpvCodes,procedureType,contractType,link",
        },
    },
    {
        "id": "tenderstream",
        "name": "Tenderstream",
        "url": "https://tenderstream.com",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .tender-item, tr.tender-row",
            "title_selector": "h2, h3, td.title",
            "link_selector": "a",
            "date_selector": ".date, td.deadline",
        },
    },
    {
        "id": "sam_gov",
        "name": "SAM.gov – US Federal Procurement",
        "url": "https://sam.gov/api/prod/sgs/v1/search/",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "sam",
            "keywords": ["architectural services", "interior design", "urban planning", "design services"],
            "naics": ["541310", "541320", "541330"],
        },
    },
    {
        "id": "contracts_finder",
        "name": "Contracts Finder – UK",
        "url": "https://www.contractsfinder.service.gov.uk/Published/Notices/PublishedNoticesSearchV2",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "contracts_finder",
            "keywords": ["architectural services", "architecture", "interior design"],
        },
    },
    {
        "id": "chilecompra",
        "name": "ChileCompra",
        "url": "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "chilecompra",
            "keywords": ["arquitectura", "diseño arquitectónico", "diseño interior"],
        },
    },
    {
        "id": "peru_seace",
        "name": "Perú SEACE",
        "url": "https://prodapp2.seace.gob.pe",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr.grilla, .convocatoria",
            "title_selector": "td, .descripcion",
            "link_selector": "a",
            "date_selector": ".fecha",
        },
    },
    {
        "id": "mexico_compranet",
        "name": "México CompraNet",
        "url": "https://compranet.hacienda.gob.mx/esop/guest/go/opportunity/search",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr.row, .opportunity-item",
            "title_selector": "td.name, .title",
            "link_selector": "a",
            "date_selector": ".date, td.fecha",
        },
    },

    # ─── SPAIN – COLEGIOS DE ARQUITECTOS ────────────────────────────────────

    {
        "id": "coam",
        "name": "COAM – Madrid",
        "url": "https://www.coam.org/es/servicios/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso-item, li.item",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": ".date, .fecha",
        },
    },
    {
        "id": "coac",
        "name": "COAC – Barcelona",
        "url": "https://www.arquitectes.cat/serveis/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurs, .item",
            "title_selector": "h2, h3",
            "link_selector": "a",
            "date_selector": ".data, time",
        },
    },
    {
        "id": "coacv",
        "name": "CTAV / COACV – Valencia & Alicante",
        "url": "https://www.coacv.org/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, .item",
            "title_selector": "h2, h3",
            "link_selector": "a",
            "date_selector": "time, .fecha",
        },
    },
    {
        "id": "coas",
        "name": "COAS – Sevilla",
        "url": "https://coas.es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso-item",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": ".date, time",
        },
    },
    {
        "id": "coavn",
        "name": "COAVN – Bilbao / País Vasco",
        "url": "https://www.coavn.org/coavn/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso",
            "title_selector": "h2, h3",
            "link_selector": "a",
            "date_selector": "time, .fecha",
        },
    },
    {
        "id": "coaa",
        "name": "COAA – Zaragoza",
        "url": "https://www.coaaragon.es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .item, li",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": ".date, time",
        },
    },
    {
        "id": "coa_malaga",
        "name": "COA Málaga",
        "url": "https://coamalaga.es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso",
            "title_selector": "h2, h3",
            "link_selector": "a",
            "date_selector": "time, .date",
        },
    },

    # ─── COLOMBIA – COMPETITIONS ─────────────────────────────────────────────

    {
        "id": "sca",
        "name": "SCA – Sociedad Colombiana de Arquitectos",
        "url": "https://sociedadcolombianadearquitectos.org/concursos",
        "category": "architecture_competition",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, .post",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": ".date, time, .entry-date",
        },
    },

    # ─── COLOMBIA – PUBLIC TENDERS ───────────────────────────────────────────

    {
        "id": "secop1",
        "name": "SECOP I",
        "url": "https://www.contratos.gov.co/consultas/inicioConsulta.do",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "api",
        "api_config": {
            "type": "secop1",
            "endpoint": "https://www.datos.gov.co/resource/jbjy-vk9h.json",
            "keywords": [
                "estudios y diseños", "diseño arquitectónico", "diseño urbano",
                "diseño interior", "estudios técnicos", "arquitectura",
            ],
            "modalidad": ["Concurso de méritos", "Selección abreviada", "Licitación pública"],
        },
    },
    {
        "id": "secop2",
        "name": "SECOP II",
        "url": "https://www.colombiacompra.gov.co/secop-ii",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "api",
        "api_config": {
            "type": "secop2",
            "endpoint": "https://www.datos.gov.co/resource/p6dx-8zbt.json",
            "keywords": [
                "estudios y diseños", "diseño arquitectónico", "diseño urbano",
                "diseño interior", "estudios técnicos", "arquitectura",
            ],
        },
    },
    {
        "id": "davibank_anim",
        "name": "Fiduciaria DAVIbank – ANIM / Virgilio Barco",
        "url": "https://www.fiducoldex.com.co/procesos",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .proceso-item, article",
            "title_selector": "td, h3, .title",
            "link_selector": "a",
            "date_selector": ".fecha, td.date",
        },
        "notes": "Monitor for architectural design commissions via autonomous heritage funds",
    },
]
