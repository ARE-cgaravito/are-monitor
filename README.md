# ARE Opportunity Monitor

Automated business development intelligence for ARE (Arquitectura, Realización y Estrategia).

Monitors 20+ architecture competition and procurement portals twice a week,
filters opportunities through Claude AI using firm-specific criteria,
and delivers a ranked digest to `contacto@are-co.com`.

## Categories monitored
- Architecture & interior design competitions — International
- Architecture & interior design competitions — Colombia & Spain
- Public and private tenders — International  
- Public and private tenders — Colombia (SECOP I, SECOP II)

## Setup
See [SETUP.md](SETUP.md) for complete step-by-step instructions.

## Schedule
Runs automatically every Monday and Thursday at 7:00 AM COT.
Can also be triggered manually from the Actions tab.

## Tech stack
- GitHub Actions (scheduler — free)
- Python 3.11 (fetcher + orchestration)
- Claude Sonnet 4.6 via Anthropic API (AI filter)
- SendGrid (email delivery — free tier)
