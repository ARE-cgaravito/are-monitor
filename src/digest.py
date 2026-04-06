"""
ARE Monitor — Email Digest Builder
Generates the HTML email and plain text summary.
"""

from datetime import datetime
import pytz

COLOMBIA_TZ = pytz.timezone("America/Bogota")

CATEGORY_LABELS = {
    "arch_competition_international": "Architecture & Design Competitions — International",
    "arch_competition_colombia": "Architecture & Design Competitions — Colombia & Spain",
    "tender_international": "Tenders — International",
    "tender_colombia": "Tenders — Colombia",
}

CATEGORY_COLORS = {
    "arch_competition_international": "#1D9E75",   # teal
    "arch_competition_colombia": "#0F6E56",         # dark teal
    "tender_international": "#D85A30",              # coral
    "tender_colombia": "#993C1D",                   # dark coral
}

CATEGORY_ORDER = [
    "tender_colombia",
    "arch_competition_colombia",
    "tender_international",
    "arch_competition_international",
]

FIT_STARS = {5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆", 1: "★☆☆☆☆"}
FIT_COLOR = {5: "#0F6E56", 4: "#1D9E75", 3: "#BA7517", 2: "#993C1D", 1: "#888780"}


def build_digest(results: dict) -> tuple[str, str]:
    """
    Returns (html_body, plain_text_body) for the email.
    """
    now = datetime.now(tz=COLOMBIA_TZ)
    run_date = now.strftime("%A %d %B %Y — %I:%M %p COT")

    included = results.get("included", [])
    borderline = results.get("borderline", [])
    total_fetched = results.get("total_fetched", 0)
    errors = results.get("errors", [])

    html = _build_html(included, borderline, total_fetched, errors, run_date)
    text = _build_text(included, borderline, total_fetched, run_date)
    return html, text


def _build_html(included, borderline, total_fetched, errors, run_date) -> str:
    sections = ""

    # Group included by category, in priority order
    by_category = {}
    for item in included:
        cat = item.get("category", "tender_colombia")
        by_category.setdefault(cat, []).append(item)

    for cat in CATEGORY_ORDER:
        items = by_category.get(cat, [])
        if not items:
            continue
        color = CATEGORY_COLORS.get(cat, "#533AB7")
        label = CATEGORY_LABELS.get(cat, cat)
        sections += f"""
        <tr><td style="padding: 28px 0 8px 0;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:4px;height:22px;background:{color};border-radius:2px;display:inline-block;"></div>
            <span style="font-size:13px;font-weight:600;color:{color};letter-spacing:0.04em;text-transform:uppercase;">{label}</span>
          </div>
        </td></tr>
        """
        for item in items:
            sections += _opportunity_card(item, color)

    # Borderline section
    if borderline:
        sections += f"""
        <tr><td style="padding: 28px 0 8px 0;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:4px;height:22px;background:#BA7517;border-radius:2px;display:inline-block;"></div>
            <span style="font-size:13px;font-weight:600;color:#BA7517;letter-spacing:0.04em;text-transform:uppercase;">⚠ Borderline — Your call</span>
          </div>
          <p style="font-size:12px;color:#888;margin:4px 0 0 14px;">These passed the core filter but have complicating factors. Review and decide.</p>
        </td></tr>
        """
        for item in borderline:
            sections += _opportunity_card(item, "#BA7517", is_borderline=True)

    # Errors
    error_html = ""
    if errors:
        error_items = "".join(f"<li style='font-size:12px;color:#999;'>{e}</li>" for e in errors)
        error_html = f"""
        <tr><td style="padding:12px 0 0 0;">
          <details>
            <summary style="font-size:11px;color:#aaa;cursor:pointer;">⚠ {len(errors)} fetch error(s)</summary>
            <ul style="margin:4px 0 0 0;">{error_items}</ul>
          </details>
        </td></tr>
        """

    total_included = len(included)
    total_borderline = len(borderline)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ARE Opportunity Digest</title>
</head>
<body style="margin:0;padding:0;background:#f5f4f0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f4f0;padding:24px 0;">
    <tr><td align="center">
      <table width="640" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;">

        <!-- HEADER -->
        <tr><td style="background:#1a1a18;border-radius:12px 12px 0 0;padding:28px 32px 24px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
              <span style="font-size:11px;color:#666;letter-spacing:0.08em;text-transform:uppercase;">Business Intelligence</span>
              <h1 style="margin:4px 0 0;font-size:22px;color:#fff;font-weight:500;letter-spacing:-0.02em;">ARE Opportunity Digest</h1>
            </div>
            <span style="font-size:11px;color:#555;margin-top:4px;">{run_date}</span>
          </div>
          <div style="margin-top:18px;display:flex;gap:16px;flex-wrap:wrap;">
            <div style="background:#2a2a28;border-radius:8px;padding:10px 16px;">
              <div style="font-size:24px;font-weight:500;color:#fff;">{total_included}</div>
              <div style="font-size:11px;color:#666;margin-top:2px;">Qualified opportunities</div>
            </div>
            <div style="background:#2a2a28;border-radius:8px;padding:10px 16px;">
              <div style="font-size:24px;font-weight:500;color:#BA7517;">{total_borderline}</div>
              <div style="font-size:11px;color:#666;margin-top:2px;">Borderline — review</div>
            </div>
            <div style="background:#2a2a28;border-radius:8px;padding:10px 16px;">
              <div style="font-size:24px;font-weight:500;color:#555;">{total_fetched}</div>
              <div style="font-size:11px;color:#666;margin-top:2px;">Total items scanned</div>
            </div>
          </div>
        </td></tr>

        <!-- BODY -->
        <tr><td style="background:#fff;padding:8px 32px 32px;border-radius:0 0 12px 12px;">
          <table width="100%" cellpadding="0" cellspacing="0">
            {sections}
            {error_html}
          </table>
        </td></tr>

        <!-- FOOTER -->
        <tr><td style="padding:16px 0;text-align:center;">
          <p style="font-size:11px;color:#aaa;margin:0;">
            ARE Monitor · Automated by Claude Sonnet · 
            <a href="https://github.com/ARE-cgaravito/are-monitor" style="color:#888;">View on GitHub</a>
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _opportunity_card(item: dict, accent_color: str, is_borderline: bool = False) -> str:
    title = item.get("title", "Untitled")
    source = item.get("source", "")
    source_url = item.get("source_url") or item.get("url", "#")
    country = item.get("country", "")
    organizer = item.get("organizer", "")
    scope = item.get("scope_summary", "")
    why = item.get("why_included", "")
    deadline = item.get("deadline", "")
    days = item.get("days_remaining")
    budget = item.get("budget", "")
    fit = item.get("strategic_fit", 0)
    flags = item.get("flags", [])

    # Deadline display
    deadline_html = ""
    if deadline:
        days_color = "#E24B4A" if days is not None and days < 10 else ("#BA7517" if days is not None and days < 21 else "#1D9E75")
        days_label = f"({days}d)" if days is not None else ""
        deadline_html = f'<span style="color:{days_color};font-weight:500;">{deadline[:10]} {days_label}</span>'
    else:
        deadline_html = '<span style="color:#aaa;">Deadline not stated</span>'

    # Flags
    flags_html = ""
    if flags:
        flag_items = "".join(f'<span style="font-size:11px;background:#fff8e6;color:#854F0B;padding:2px 7px;border-radius:4px;margin-right:4px;">{f}</span>' for f in flags)
        flags_html = f'<div style="margin-top:8px;">{flag_items}</div>'

    # Strategic fit
    fit_html = ""
    if not is_borderline and fit:
        stars = FIT_STARS.get(fit, "")
        fc = FIT_COLOR.get(fit, "#888")
        fit_html = f'<span style="font-size:12px;color:{fc};" title="Strategic fit {fit}/5">{stars}</span>'

    meta_parts = []
    if source:
        meta_parts.append(f'<a href="{source_url}" style="color:{accent_color};text-decoration:none;font-weight:500;">{source}</a>')
    if country:
        meta_parts.append(f'<span style="color:#888;">{country}</span>')
    if organizer:
        meta_parts.append(f'<span style="color:#888;">{organizer[:60]}</span>')
    meta_html = ' · '.join(meta_parts)

    budget_html = f'<span style="color:#555;">{budget}</span> · ' if budget else ""

    return f"""
    <tr><td style="border:1px solid #ebebeb;border-radius:8px;padding:16px 18px;margin-bottom:8px;display:block;margin-top:8px;">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">
        <a href="{source_url}" style="font-size:15px;font-weight:500;color:#1a1a18;text-decoration:none;line-height:1.35;flex:1;">{title}</a>
        {fit_html}
      </div>
      <div style="font-size:12px;margin-top:6px;color:#666;">{meta_html}</div>
      {f'<p style="font-size:13px;color:#444;margin:8px 0 4px;line-height:1.5;">{scope}</p>' if scope else ""}
      {f'<p style="font-size:12px;color:#888;margin:4px 0;font-style:italic;">{why}</p>' if why else ""}
      <div style="margin-top:8px;font-size:12px;color:#666;">
        {budget_html}Deadline: {deadline_html}
      </div>
      {flags_html}
    </td></tr>
    """


def _build_text(included, borderline, total_fetched, run_date) -> str:
    lines = [
        "ARE OPPORTUNITY DIGEST",
        f"Run: {run_date}",
        f"Scanned: {total_fetched} | Qualified: {len(included)} | Borderline: {len(borderline)}",
        "=" * 60,
    ]

    by_category = {}
    for item in included:
        cat = item.get("category", "other")
        by_category.setdefault(cat, []).append(item)

    for cat in CATEGORY_ORDER:
        items = by_category.get(cat, [])
        if not items:
            continue
        lines.append(f"\n{CATEGORY_LABELS.get(cat, cat).upper()}")
        lines.append("-" * 40)
        for item in items:
            lines.append(f"\n• {item.get('title', '')}")
            lines.append(f"  Source: {item.get('source', '')} | {item.get('url', '')}")
            lines.append(f"  Deadline: {item.get('deadline', 'unknown')} | Budget: {item.get('budget', 'not stated')}")
            if item.get("scope_summary"):
                lines.append(f"  {item['scope_summary']}")
            if item.get("flags"):
                lines.append(f"  Flags: {', '.join(item['flags'])}")

    if borderline:
        lines.append(f"\n⚠ BORDERLINE — REVIEW REQUIRED")
        lines.append("-" * 40)
        for item in borderline:
            lines.append(f"\n• {item.get('title', '')}")
            lines.append(f"  Source: {item.get('source', '')} | {item.get('url', '')}")
            if item.get("flags"):
                lines.append(f"  Flags: {', '.join(item['flags'])}")

    return "\n".join(lines)
