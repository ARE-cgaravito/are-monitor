"""
ARE Monitor — Digest Builder
Generates a standalone HTML file published via GitHub Pages.
No email, no external services.
"""

from datetime import datetime
import pytz

COLOMBIA_TZ = pytz.timezone("America/Bogota")

CATEGORY_LABELS = {
    "arch_competition_international": "Architecture & Design Competitions — International",
    "arch_competition_colombia":      "Architecture & Design Competitions — Colombia & Spain",
    "tender_international":           "Tenders — International",
    "tender_colombia":                "Tenders — Colombia",
}

CATEGORY_COLORS = {
    "arch_competition_international": "#1D9E75",
    "arch_competition_colombia":      "#0F6E56",
    "tender_international":           "#D85A30",
    "tender_colombia":                "#185FA5",
}

CATEGORY_ORDER = [
    "tender_colombia",
    "arch_competition_colombia",
    "tender_international",
    "arch_competition_international",
]

FIT_STARS = {5: "★★★★★", 4: "★★★★☆", 3: "★★★☆☆", 2: "★★☆☆☆", 1: "★☆☆☆☆"}
FIT_COLOR = {5: "#0F6E56", 4: "#1D9E75", 3: "#BA7517", 2: "#993C1D", 1: "#888780"}


def build_digest(results: dict) -> str:
    """Returns the full HTML string to write to docs/index.html"""
    now = datetime.now(tz=COLOMBIA_TZ)
    run_date = now.strftime("%A %d %B %Y — %I:%M %p COT")

    included   = results.get("included", [])
    borderline = results.get("borderline", [])
    total      = results.get("total_fetched", 0)
    errors     = results.get("errors", [])

    by_cat = {}
    for item in included:
        by_cat.setdefault(item.get("category", "tender_colombia"), []).append(item)

    sections_html = ""
    for cat in CATEGORY_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        color = CATEGORY_COLORS.get(cat, "#533AB7")
        label = CATEGORY_LABELS.get(cat, cat)
        cards = "".join(_card(i, color) for i in items)
        sections_html += f"""
        <section>
          <div class="section-header">
            <div class="section-bar" style="background:{color}"></div>
            <span class="section-label" style="color:{color}">{label}</span>
            <span class="section-count" style="color:{color}">{len(items)}</span>
          </div>
          <div class="cards">{cards}</div>
        </section>"""

    if borderline:
        cards = "".join(_card(i, "#BA7517", borderline=True) for i in borderline)
        sections_html += f"""
        <section>
          <div class="section-header">
            <div class="section-bar" style="background:#BA7517"></div>
            <span class="section-label" style="color:#BA7517">Borderline — your call</span>
            <span class="section-count" style="color:#BA7517">{len(borderline)}</span>
          </div>
          <p class="borderline-note">These passed the core filter but have complicating factors. Review individually.</p>
          <div class="cards">{cards}</div>
        </section>"""

    if not included and not borderline:
        sections_html = """
        <div class="empty">
          <div class="empty-icon">—</div>
          <p>No qualifying opportunities found in this run.</p>
          <p class="empty-sub">Sources were scanned — nothing passed the filter criteria.</p>
        </div>"""

    error_html = ""
    if errors:
        items_html = "".join(f"<li>{e}</li>" for e in errors)
        error_html = f"""
        <details class="error-log">
          <summary>{len(errors)} fetch error(s) — click to expand</summary>
          <ul>{items_html}</ul>
        </details>"""

    n_inc = len(included)
    n_brd = len(borderline)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ARE Opportunity Digest</title>
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f4f3ef;color:#1a1a18;min-height:100vh}}
    .header{{background:#1a1a18;padding:32px 40px 28px}}
    .header-meta{{font-size:11px;color:#555;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px}}
    .header h1{{font-size:24px;font-weight:500;color:#fff;letter-spacing:-.02em;margin-bottom:20px}}
    .stats{{display:flex;gap:12px;flex-wrap:wrap}}
    .stat{{background:#2a2a28;border-radius:8px;padding:10px 18px;min-width:90px}}
    .stat-number{{font-size:26px;font-weight:500;color:#fff;line-height:1}}
    .stat-number.amber{{color:#BA7517}}
    .stat-number.muted{{color:#555}}
    .stat-label{{font-size:11px;color:#666;margin-top:4px}}
    .run-date{{font-size:11px;color:#444;margin-top:16px}}
    .body{{max-width:800px;margin:0 auto;padding:32px 24px 64px}}
    section{{margin-bottom:40px}}
    .section-header{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
    .section-bar{{width:4px;height:20px;border-radius:2px;flex-shrink:0}}
    .section-label{{font-size:12px;font-weight:600;letter-spacing:.05em;text-transform:uppercase}}
    .section-count{{font-size:12px;font-weight:600;background:#ebebeb;border-radius:20px;padding:1px 8px}}
    .borderline-note{{font-size:12px;color:#888;margin:-4px 0 12px 14px}}
    .cards{{display:flex;flex-direction:column;gap:8px}}
    .card{{background:#fff;border:1px solid #e8e8e4;border-radius:10px;padding:16px 20px;transition:box-shadow .15s}}
    .card:hover{{box-shadow:0 2px 12px rgba(0,0,0,.07)}}
    .card-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}}
    .card-title{{font-size:15px;font-weight:500;color:#1a1a18;text-decoration:none;line-height:1.4;flex:1}}
    .card-title:hover{{color:#185FA5}}
    .fit-stars{{font-size:13px;flex-shrink:0;margin-top:1px}}
    .card-meta{{font-size:12px;color:#888;margin-top:5px}}
    .card-meta a{{color:inherit;font-weight:500;text-decoration:none}}
    .card-meta a:hover{{text-decoration:underline}}
    .card-scope{{font-size:13px;color:#444;margin-top:8px;line-height:1.55}}
    .card-why{{font-size:12px;color:#999;font-style:italic;margin-top:4px}}
    .card-bottom{{display:flex;align-items:center;gap:12px;margin-top:10px;flex-wrap:wrap}}
    .deadline{{font-size:12px;font-weight:500}}
    .deadline.urgent{{color:#E24B4A}}
    .deadline.soon{{color:#BA7517}}
    .deadline.ok{{color:#1D9E75}}
    .deadline.unknown{{color:#aaa}}
    .budget{{font-size:12px;color:#666}}
    .flags{{display:flex;gap:4px;flex-wrap:wrap;margin-top:6px}}
    .flag{{font-size:11px;background:#fff8e6;color:#854F0B;padding:2px 8px;border-radius:4px}}
    .empty{{text-align:center;padding:80px 20px;color:#888}}
    .empty-icon{{font-size:40px;margin-bottom:16px;opacity:.3}}
    .empty-sub{{font-size:13px;margin-top:6px}}
    .error-log{{margin-top:40px;font-size:12px;color:#aaa;border-top:1px solid #e8e8e4;padding-top:16px}}
    .error-log summary{{cursor:pointer}}
    .error-log ul{{margin-top:8px;padding-left:20px}}
    .error-log li{{margin-bottom:4px}}
    .footer{{text-align:center;font-size:11px;color:#bbb;padding:20px;border-top:1px solid #e8e8e4}}
    .footer a{{color:#bbb}}
    @media(max-width:600px){{.header{{padding:24px 20px 20px}}.body{{padding:24px 16px 48px}}.header h1{{font-size:20px}}}}
  </style>
</head>
<body>
  <div class="header">
    <div class="header-meta">Business Intelligence · ARE</div>
    <h1>Opportunity Digest</h1>
    <div class="stats">
      <div class="stat"><div class="stat-number">{n_inc}</div><div class="stat-label">Qualified</div></div>
      <div class="stat"><div class="stat-number amber">{n_brd}</div><div class="stat-label">Borderline</div></div>
      <div class="stat"><div class="stat-number muted">{total}</div><div class="stat-label">Scanned</div></div>
    </div>
    <div class="run-date">Last updated: {run_date}</div>
  </div>
  <div class="body">
    {sections_html}
    {error_html}
  </div>
  <div class="footer">
    ARE Monitor · Powered by Claude Sonnet ·
    <a href="https://github.com/ARE-cgaravito/are-monitor">GitHub</a>
  </div>
</body>
</html>"""


def _card(item: dict, accent: str, borderline: bool = False) -> str:
    title     = item.get("title", "Untitled")
    url       = item.get("source_url") or item.get("url", "#")
    source    = item.get("source", "")
    country   = item.get("country", "")
    organizer = item.get("organizer", "")
    scope     = item.get("scope_summary", "")
    why       = item.get("why_included", "")
    deadline  = item.get("deadline", "")
    days      = item.get("days_remaining")
    budget    = item.get("budget", "")
    fit       = item.get("strategic_fit", 0)
    flags     = item.get("flags", [])

    fit_html = ""
    if not borderline and fit:
        stars = FIT_STARS.get(fit, "")
        color = FIT_COLOR.get(fit, "#888")
        fit_html = f'<span class="fit-stars" style="color:{color}" title="Strategic fit {fit}/5">{stars}</span>'

    meta_parts = []
    if source:
        meta_parts.append(f'<a href="{url}" style="color:{accent}">{source}</a>')
    if country:
        meta_parts.append(country)
    if organizer:
        meta_parts.append(organizer[:60])
    meta = " · ".join(meta_parts)

    if deadline:
        if days is not None and days < 10:
            dcls, dlabel = "urgent", f"Deadline {deadline[:10]} ({days}d remaining)"
        elif days is not None and days < 21:
            dcls, dlabel = "soon",   f"Deadline {deadline[:10]} ({days}d remaining)"
        else:
            dcls, dlabel = "ok",     f"Deadline {deadline[:10]}"
    else:
        dcls, dlabel = "unknown", "Deadline not stated"

    budget_html = f'<span class="budget">{budget}</span>' if budget else ""
    flags_html = ""
    if flags:
        flag_items = "".join(f'<span class="flag">{f}</span>' for f in flags)
        flags_html = f'<div class="flags">{flag_items}</div>'

    return f"""
    <div class="card">
      <div class="card-top">
        <a class="card-title" href="{url}" target="_blank" rel="noopener">{title}</a>
        {fit_html}
      </div>
      <div class="card-meta">{meta}</div>
      {f'<p class="card-scope">{scope}</p>' if scope else ""}
      {f'<p class="card-why">{why}</p>'     if why   else ""}
      <div class="card-bottom">
        <span class="deadline {dcls}">{dlabel}</span>
        {budget_html}
      </div>
      {flags_html}
    </div>"""
