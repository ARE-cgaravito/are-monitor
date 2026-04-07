# ARE Monitor — Source Configuration v5
# 35 sources across 6 categories

SOURCES = [

    # ═══════════════════════════════════════════════════════════════════════
    # INTERNATIONAL ARCHITECTURE & DESIGN COMPETITIONS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "bustler",
        "name": "Bustler",
        "url": "https://bustler.net/competitions/type/0/page/1",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "timeout": 30,
        "scrape_config": {
            "listing_selector": "article, .comp-item, .item, li",
            "title_selector": "h2, h3, .item-title, a",
            "link_selector": "a",
            "date_selector": ".date, time, .item-date",
        },
    },
    {
        "id": "archdaily_competitions",
        "name": "ArchDaily – Competitions",
        "url": "https://www.archdaily.com/search/competitions",
        "rss": "https://www.archdaily.com/feed",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "competitions_archi",
        "name": "Competitions.Archi",
        "url": "https://competitions.archi",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition-item, .card, .post",
            "title_selector": "h2, h3, .title, .entry-title",
            "link_selector": "a",
            "date_selector": ".date, time, .deadline",
        },
    },
    {
        "id": "world_architecture",
        "name": "World Architecture Competitions",
        "url": "https://worldarchitecture.org/architecture-competitions",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "div.compWrap, article, .competition, li",
            "title_selector": "h2, h3, .compTitle, a",
            "link_selector": "a",
            "date_selector": ".date, .deadline, span",
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
            "listing_selector": "article, .competition-item, li.views-row, .node",
            "title_selector": "h2, h3, .views-field-title, .field-name-title",
            "link_selector": "a",
            "date_selector": ".date-display-single, .field-name-field-date, time",
        },
    },
    {
        "id": "europaconcorsi",
        "name": "Europaconcorsi",
        "url": "https://europaconcorsi.com/en/competitions/latest",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition, .event, li.item",
            "title_selector": "h2, h3, .title, .competition-title",
            "link_selector": "a",
            "date_selector": "time, .date, .deadline",
        },
    },
    {
        "id": "archinect_competitions",
        "name": "Archinect – Competitions",
        "url": "https://archinect.com/competitions",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .post, .open-call",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": "time, .date, .entry-date",
        },
    },
    {
        "id": "riba_competitions",
        "name": "RIBA Competitions",
        "url": "https://www.riba.org/explore/competitions/",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition-item, .card, li",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": "time, .date, .deadline",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # INTERNATIONAL TENDERS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "ted",
        "name": "TED – Tenders Electronic Daily (EU)",
        "url": "https://ted.europa.eu/en/search/result?scope=1&query=71220000+OR+71240000+OR+71400000&onlyLatest=true",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .notice-item, li.result, tr",
            "title_selector": "h2, h3, .notice-title, td.title, a",
            "link_selector": "a",
            "date_selector": ".date, .publication-date, td, time",
        },
    },
    {
        "id": "contratacion_estado_spain",
        "name": "Plataforma Contratación del Estado – Spain",
        "url": "https://contrataciondelestado.es/wps/portal/plataforma",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .licitacion, .expediente, li",
            "title_selector": "td, .titulo, h3, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "contracts_finder",
        "name": "Contracts Finder – UK",
        "url": "https://www.contractsfinder.service.gov.uk",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "contracts_finder",
            "keywords": ["architectural services", "architecture", "interior design"],
        },
    },
    {
        "id": "idb_projects",
        "name": "IDB – Inter-American Development Bank",
        "url": "https://www.iadb.org/en/project-search?query=architecture+design&sector=Urban+Development+and+Housing",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .project-item, .search-result, li, tr",
            "title_selector": "h2, h3, .project-title, td, a",
            "link_selector": "a",
            "date_selector": ".date, td, time",
        },
    },
    {
        "id": "world_bank",
        "name": "World Bank – Consulting Opportunities",
        "url": "https://projects.worldbank.org/en/projects-operations/procurement",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .notice-item, article, li",
            "title_selector": "td, h3, .title, a",
            "link_selector": "a",
            "date_selector": ".date, td, time",
        },
    },
    {
        "id": "ungm",
        "name": "UNGM – UN Global Marketplace",
        "url": "https://www.ungm.org/Public/Notice",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .notice-row, li",
            "title_selector": "td, .title, a",
            "link_selector": "a",
            "date_selector": ".date, td",
        },
    },
    {
        "id": "tenderstream",
        "name": "Tenderstream – Public Listings",
        "url": "https://tenderstream.com/tenders",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .tender-item, .tender, li.item, tr",
            "title_selector": "h2, h3, .tender-title, td.title, a",
            "link_selector": "a",
            "date_selector": ".date, .deadline, td.date, time",
        },
        "notes": "Public listings only — upgrade to paid for full access",
    },
    {
        "id": "chilecompra",
        "name": "ChileCompra",
        "url": "https://api.mercadopublico.cl",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "api",
        "api_config": {
            "type": "chilecompra",
            "keywords": ["arquitectura", "diseño arquitectónico"],
        },
    },
    {
        "id": "peru_seace",
        "name": "Perú SEACE",
        "url": "https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .convocatoria, .item",
            "title_selector": "td, .descripcion, h3",
            "link_selector": "a",
            "date_selector": ".fecha, td",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # SPAIN – COLEGIOS DE ARQUITECTOS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "concursos_arquitectura",
        "name": "ConcursosArquitectura.com",
        "url": "https://concursosdearquitectura.com",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, .post, li",
            "title_selector": "h2, h3, .entry-title, .title",
            "link_selector": "a",
            "date_selector": "time, .date, .entry-date",
        },
    },
    {
        "id": "coam",
        "name": "COAM – Madrid",
        "url": "https://www.coam.org/es/servicios/concursos-de-arquitectura",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso-item, li.item, .views-row",
            "title_selector": "h2, h3, .title, .views-field-title",
            "link_selector": "a",
            "date_selector": ".date, .fecha, time",
        },
    },
    {
        "id": "coac",
        "name": "COAC – Barcelona",
        "url": "https://www.arquitectes.cat/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurs, .item, li",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": ".data, time, .date",
        },
    },
    {
        "id": "coacv",
        "name": "CTAV / COACV – Valencia & Alicante",
        "url": "https://www.coacv.org/es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, .item, li",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": "time, .fecha, .date",
        },
    },
    {
        "id": "coas",
        "name": "COAS – Sevilla",
        "url": "https://coas.es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "verify_ssl": False,
        "scrape_config": {
            "listing_selector": "article, .concurso-item, .post",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": ".date, time",
        },
    },
    {
        "id": "coavn",
        "name": "COAVN – Bilbao / País Vasco",
        "url": "https://www.coavn.org/es/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, li, .item",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": "time, .fecha",
        },
    },
    {
        "id": "coaa",
        "name": "COAA – Zaragoza",
        "url": "https://www.coaaragon.es/coaaragon/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .item, li, .concurso",
            "title_selector": "h2, h3, .title",
            "link_selector": "a",
            "date_selector": ".date, time",
        },
    },
    {
        "id": "coa_malaga",
        "name": "COA Málaga",
        "url": "https://coamalaga.es/servicios/concursos",
        "category": "architecture_competition",
        "subcategory": "spain",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, li, .post",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": "time, .date",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # COLOMBIA – COMPETITIONS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "sca",
        "name": "SCA – Sociedad Colombiana de Arquitectos",
        "url": "https://sociedadcolombianadearquitectos.org/concursos/",
        "category": "architecture_competition",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .concurso, .post, li",
            "title_selector": "h2, h3, .entry-title, .title",
            "link_selector": "a",
            "date_selector": ".date, time, .entry-date",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # COLOMBIA – PUBLIC TENDERS (SECOP + KEY ENTITIES)
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "secop_integrado",
        "name": "SECOP Integrado (I + II)",
        "url": "https://www.datos.gov.co/resource/rpmr-utcd.json",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "api",
        "api_config": {
            "type": "secop_integrado",
            "endpoint": "https://www.datos.gov.co/resource/rpmr-utcd.json",
            "keywords": [
                "estudios y diseños",
                "diseño arquitectónico",
                "diseño urbano",
                "diseño interior",
                "arquitectura",
            ],
        },
    },
    {
        "id": "findeter",
        "name": "Findeter – Financiera de Desarrollo Territorial",
        "url": "https://www.findeter.gov.co/contratacion",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, .proceso, li, .contrato",
            "title_selector": "h2, h3, td, .titulo, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "eru_bogota",
        "verify_ssl": False,
        "name": "ERU – Empresa de Renovación Urbana de Bogotá",
        "url": "https://www.eru.gov.co/es/procesos-de-contratacion",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, .proceso, li",
            "title_selector": "h2, h3, td, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "alcaldia_medellin",
        "name": "Alcaldía de Medellín – Contratación",
        "url": "https://www.medellin.gov.co/irj/portal/medellin?NavigationTarget=navurl://6ec7d3c2dae3e88a6c3c24c9df04d73e",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, li, .proceso",
            "title_selector": "h2, h3, td, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "davibank_anim",
        "name": "Fiduciaria Davivienda – Patrimonios Autónomos",
        "url": "https://www.davibank.com/fiduciaria/publica/productos/patrimonios-autonomos",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .proceso-item, article, li",
            "title_selector": "td, h3, .title, a",
            "link_selector": "a",
            "date_selector": ".fecha, td.date, time",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # LATIN AMERICA — COUNTRY PROCUREMENT PORTALS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "ecuador_sercop",
        "name": "Ecuador – SERCOP (Compras Públicas)",
        "url": "https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/buscarProceso.cpe",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .proceso, .item, li",
            "title_selector": "td, .descripcion, h3, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "guyana_npta",
        "name": "Guyana – National Procurement & Tender Administration",
        "url": "http://guyanapo.gov.gy/tenders/",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, li, .tender",
            "title_selector": "h2, h3, td, a, .title",
            "link_selector": "a",
            "date_selector": ".date, td, time",
        },
    },
    {
        "id": "dominican_republic_dgcp",
        "name": "República Dominicana – DGCP",
        "url": "https://www.dgcp.gob.do/oportunidades-de-negocio/",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, li, .proceso",
            "title_selector": "h2, h3, td, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },
    {
        "id": "mexico_compranet",
        "name": "México – CompraNet",
        "url": "https://www.infomex.org.mx/gobiernofederal/moduloPublico/moduloPublico.action",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "tr, .licitacion, li",
            "title_selector": "td, h3, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # HOSPITALITY — INDUSTRY PIPELINE & PRESS
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "hospitalitynet",
        "name": "Hospitalitynet – Hotel Development News",
        "url": "https://www.hospitalitynet.org/news/hotel_development.html",
        "rss": "https://www.hospitalitynet.org/rss/4development.html",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "hotel_management_dev",
        "name": "Hotel Management – Development",
        "url": "https://www.hotelmanagement.net/development",
        "rss": "https://www.hotelmanagement.net/rss.xml",
        "category": "tender",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "sleeper_news",
        "name": "Sleeper Magazine – Hospitality Design",
        "url": "https://sleeper.media",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .post, .news-item",
            "title_selector": "h2, h3, .entry-title",
            "link_selector": "a",
            "date_selector": "time, .date",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # COLOMBIA — HOSPITALITY & TOURISM SECTOR
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "fontur",
        "name": "FONTUR Colombia – Fondo Nacional de Turismo",
        "url": "https://fontur.com.co/contratacion",
        "category": "tender",
        "subcategory": "colombia",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, tr, li, .proceso",
            "title_selector": "h2, h3, td, a",
            "link_selector": "a",
            "date_selector": ".fecha, td, time",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════
    # NEW INTERNATIONAL COMPETITION SOURCES
    # ═══════════════════════════════════════════════════════════════════════

    {
        "id": "dezeen_competitions",
        "name": "Dezeen Competitions",
        "url": "https://www.dezeen.com/competitions/",
        "rss": "https://www.dezeen.com/competitions/feed/",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "designboom_competitions",
        "name": "Designboom – Competitions",
        "url": "https://www.designboom.com/competition/",
        "rss": "https://www.designboom.com/competition/feed/",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "rss",
    },
    {
        "id": "architects_journal",
        "name": "Architects Journal – Competitions",
        "url": "https://www.architectsjournal.co.uk/competitions",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .competition-item, .card, li",
            "title_selector": "h2, h3, .title, a",
            "link_selector": "a",
            "date_selector": "time, .date, .deadline",
        },
    },
    {
        "id": "amsterdam_competitions",
        "name": "City of Amsterdam – Open Calls",
        "url": "https://www.amsterdam.nl/prijsvragen/",
        "category": "architecture_competition",
        "subcategory": "international",
        "fetch_method": "scrape",
        "scrape_config": {
            "listing_selector": "article, .item, li, .prijsvraag",
            "title_selector": "h2, h3, .title, a",
            "link_selector": "a",
            "date_selector": "time, .date, .deadline",
        },
    },
]
