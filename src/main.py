"""
ARE Monitor — Main Entry Point
Orchestrates: fetch → filter → digest → send
"""

import os
import sys
import json
import logging
from datetime import datetime
import pytz

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.sources import SOURCES
from src.fetcher import fetch_source
from src.filter import filter_opportunities
from src.digest import build_digest
from src.mailer import send_digest

# ─── LOGGING ──────────────────────────────────────────────────────────────────

os.makedirs("logs", exist_ok=True)
COLOMBIA_TZ = pytz.timezone("America/Bogota")
log_filename = f"logs/run_{datetime.now(tz=COLOMBIA_TZ).strftime('%Y%m%d_%H%M')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("are-monitor")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    start = datetime.now(tz=COLOMBIA_TZ)
    logger.info(f"═══ ARE Monitor run started: {start.strftime('%A %d %B %Y %H:%M COT')} ═══")
    logger.info(f"Sources configured: {len(SOURCES)}")

    # ── Step 1: Fetch all sources ──────────────────────────────────────────────
    all_raw = []
    fetch_errors = []

    for source in SOURCES:
        logger.info(f"Fetching [{source['id']}] {source['name']}...")
        try:
            items = fetch_source(source, since_hours=96)  # last 4 days on each run
            all_raw.extend(items)
        except Exception as e:
            msg = f"Fetch failed for {source['id']}: {e}"
            logger.error(msg)
            fetch_errors.append(msg)

    logger.info(f"Total raw items fetched: {len(all_raw)}")

    if not all_raw:
        logger.warning("No items fetched from any source — sending empty digest")

    # ── Step 2: Deduplicate by URL/ID ─────────────────────────────────────────
    seen_ids = set()
    unique_raw = []
    for item in all_raw:
        uid = item.get("id") or item.get("url")
        if uid and uid not in seen_ids:
            seen_ids.add(uid)
            unique_raw.append(item)

    logger.info(f"After deduplication: {len(unique_raw)} unique items")

    # ── Step 3: Filter via Claude ──────────────────────────────────────────────
    results = filter_opportunities(unique_raw)
    results["errors"] = results.get("errors", []) + fetch_errors

    logger.info(
        f"Filter complete: {len(results['included'])} INCLUDE, "
        f"{len(results['borderline'])} BORDERLINE, "
        f"{len(results['excluded'])} EXCLUDE"
    )

    # ── Step 4: Save results JSON ──────────────────────────────────────────────
    results_file = f"logs/results_{datetime.now(tz=COLOMBIA_TZ).strftime('%Y%m%d_%H%M')}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info(f"Results saved to {results_file}")

    # ── Step 5: Build digest ───────────────────────────────────────────────────
    html_body, text_body = build_digest(results)

    # ── Step 6: Send email ─────────────────────────────────────────────────────
    send_digest(html_body, text_body, results)

    # ── Done ───────────────────────────────────────────────────────────────────
    elapsed = (datetime.now(tz=COLOMBIA_TZ) - start).seconds
    logger.info(f"═══ Run complete in {elapsed}s ═══")


if __name__ == "__main__":
    main()
