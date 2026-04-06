"""
ARE Monitor — Claude Filter Module
Sends opportunity batches to Claude Sonnet and returns structured decisions.
"""

import anthropic
import json
import logging
import os
from datetime import datetime
import pytz

from config.prompt import SYSTEM_PROMPT, build_user_message

logger = logging.getLogger(__name__)
COLOMBIA_TZ = pytz.timezone("America/Bogota")
BATCH_SIZE = 10  # opportunities per Claude call (stay well within context)


def filter_opportunities(raw_opportunities: list) -> dict:
    """
    Main function. Takes raw fetched opportunities, sends to Claude in batches,
    returns structured dict with included, borderline, excluded lists.
    """
    if not raw_opportunities:
        logger.info("No opportunities to filter.")
        return {"included": [], "borderline": [], "excluded": [], "errors": []}

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    all_results = []
    errors = []

    # Process in batches
    batches = [raw_opportunities[i:i+BATCH_SIZE] for i in range(0, len(raw_opportunities), BATCH_SIZE)]
    logger.info(f"Filtering {len(raw_opportunities)} opportunities in {len(batches)} batches")

    for batch_num, batch in enumerate(batches, 1):
        logger.info(f"  Sending batch {batch_num}/{len(batches)} ({len(batch)} items) to Claude...")
        try:
            user_msg = build_user_message(batch)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )

            raw_text = response.content[0].text.strip()

            # Strip markdown code fences if present
            if raw_text.startswith("```"):
                lines = raw_text.split("\n")
                raw_text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

            evaluated = json.loads(raw_text)

            # Add days_remaining if we have a deadline and it's not already set
            today = datetime.now(tz=COLOMBIA_TZ).date()
            for item in evaluated:
                if item.get("deadline") and item.get("days_remaining") is None:
                    try:
                        dl = datetime.strptime(item["deadline"][:10], "%Y-%m-%d").date()
                        item["days_remaining"] = (dl - today).days
                    except Exception:
                        pass

            all_results.extend(evaluated)

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error on batch {batch_num}: {e}")
            errors.append(f"Batch {batch_num}: JSON parse failed — {e}")
        except Exception as e:
            logger.error(f"Claude API error on batch {batch_num}: {e}")
            errors.append(f"Batch {batch_num}: API error — {e}")

    # Split by decision
    included = [r for r in all_results if r.get("decision") == "INCLUDE"]
    borderline = [r for r in all_results if r.get("decision") == "BORDERLINE"]
    excluded = [r for r in all_results if r.get("decision") == "EXCLUDE"]

    # Sort included by strategic_fit desc, then days_remaining asc
    included.sort(key=lambda x: (-x.get("strategic_fit", 0), x.get("days_remaining") or 999))
    borderline.sort(key=lambda x: x.get("days_remaining") or 999)

    logger.info(
        f"Filter results: {len(included)} included, {len(borderline)} borderline, "
        f"{len(excluded)} excluded, {len(errors)} errors"
    )

    return {
        "included": included,
        "borderline": borderline,
        "excluded": excluded,
        "errors": errors,
        "total_fetched": len(raw_opportunities),
    }
