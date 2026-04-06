"""
ARE Monitor — Email Sender
Uses SendGrid free tier (100 emails/day).
"""

import os
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)
COLOMBIA_TZ = pytz.timezone("America/Bogota")


def send_digest(html_body: str, text_body: str, results: dict):
    """Send the digest email via SendGrid."""
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail, Content, MimeType
    except ImportError:
        logger.error("sendgrid package not installed")
        return

    api_key = os.environ.get("SENDGRID_API_KEY")
    to_email = os.environ.get("DIGEST_EMAIL", "contacto@are-co.com")
    from_email = os.environ.get("FROM_EMAIL", "monitor@are-co.com")

    if not api_key:
        logger.error("SENDGRID_API_KEY not set — skipping email")
        return

    now = datetime.now(tz=COLOMBIA_TZ)
    day_name = now.strftime("%A")
    date_str = now.strftime("%d %b %Y")

    n_included = len(results.get("included", []))
    n_borderline = len(results.get("borderline", []))

    if n_included == 0 and n_borderline == 0:
        subject = f"ARE Monitor — {day_name} {date_str} — No new opportunities"
    else:
        subject = f"ARE Monitor — {day_name} {date_str} — {n_included} opportunities, {n_borderline} borderline"

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
    )
    message.content = [
        Content(MimeType.text, text_body),
        Content(MimeType.html, html_body),
    ]

    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        response = sg.send(message)
        logger.info(f"Email sent → {to_email} (status {response.status_code})")
    except Exception as e:
        logger.error(f"SendGrid error: {e}")
