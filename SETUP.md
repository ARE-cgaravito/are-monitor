# ARE Opportunity Monitor — Complete Setup Guide

## What this system does
Twice a week (Monday and Thursday at 7 AM Bogotá time), this system:
1. Visits 20+ architecture and procurement websites automatically
2. Sends every new listing to Claude AI for intelligent filtering
3. Emails you a ranked digest of only the opportunities that matter to ARE

Estimated running cost: **~$1–3 USD/month** (Claude API only — everything else is free)

---

## BEFORE YOU START — Get your API keys

You need three things. Do this first.

### A) Anthropic API key (Claude)
1. Go to https://console.anthropic.com
2. Sign up / log in
3. Click **API Keys** in the left sidebar
4. Click **Create Key** — name it "ARE Monitor"
5. **Copy the key now** — it starts with `sk-ant-...`
6. ⚠️ You will need to add a credit card and load credits ($5 is enough for months)

### B) SendGrid API key (free email delivery)
1. Go to https://sendgrid.com and create a free account
2. Go to **Settings → API Keys**
3. Click **Create API Key** → choose "Restricted Access" → enable "Mail Send"
4. **Copy the key** — it starts with `SG.`
5. **Important**: go to **Settings → Sender Authentication** and verify `contacto@are-co.com`
   as your sender email (SendGrid will send you a confirmation link)

---

## STEP 1 — Create the GitHub repository

1. Go to https://github.com/ARE-cgaravito
2. Click the **+** button (top right) → **New repository**
3. Name it exactly: `are-monitor`
4. Set it to **Private** (important — your config is here)
5. Do NOT check "Initialize with README"
6. Click **Create repository**

---

## STEP 2 — Upload the code

### Option A: Using GitHub's web interface (easiest, no technical knowledge needed)

1. On your new empty repository page, click **uploading an existing file**
2. Open the `are-monitor` folder on your computer
3. Drag ALL files and folders into the GitHub upload area
4. Important: GitHub's web uploader doesn't handle folders well.
   Instead, use Option B below (it's only 4 commands and takes 3 minutes).

### Option B: Using GitHub Desktop (recommended — easiest visual tool)

1. Download GitHub Desktop from https://desktop.github.com
2. Install and sign in with your `ARE-cgaravito` account
3. Click **File → Clone Repository** → find `are-monitor`
4. Choose where to save it on your computer
5. Copy all the files from the `are-monitor` folder you received into that cloned folder
6. In GitHub Desktop, you'll see all files listed as "changes"
7. Write "Initial setup" in the Summary box at bottom left
8. Click **Commit to main**
9. Click **Push origin** (blue button)
10. Done — your code is now on GitHub ✅

---

## STEP 3 — Add your secret API keys to GitHub

This is how you give the system your API keys securely
(they never appear in your code — they're stored encrypted by GitHub).

1. Go to your repository: `https://github.com/ARE-cgaravito/are-monitor`
2. Click **Settings** (top menu of the repo)
3. In the left sidebar, click **Secrets and variables → Actions**
4. Click **New repository secret** and add these THREE secrets one by one:

| Secret Name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your Claude API key (`sk-ant-...`) |
| `SENDGRID_API_KEY` | Your SendGrid key (`SG.xxx...`) |
| `DIGEST_EMAIL` | `contacto@are-co.com` |

For each one: click "New repository secret", type the Name exactly as shown,
paste your Value, click "Add secret".

---

## STEP 4 — Enable GitHub Actions

1. In your repository, click the **Actions** tab (top menu)
2. If you see a yellow banner asking you to enable workflows, click **Enable**
3. You should see "ARE Opportunity Monitor" in the left sidebar

---

## STEP 5 — Run your first test

Don't wait until Monday to see if it works.

1. Go to **Actions** tab
2. Click **ARE Opportunity Monitor** in the left sidebar
3. Click **Run workflow** (right side, blue button)
4. Click the green **Run workflow** button that appears
5. Watch it run (takes 3–5 minutes)
6. If it shows a green ✅ checkmark: success — check your email!
7. If it shows a red ✗: click on it to see the error log

---

## STEP 6 — Ongoing schedule

After the first successful test, the system runs automatically:
- **Every Monday at 7:00 AM COT**
- **Every Thursday at 7:00 AM COT**

You don't need to do anything. You'll receive an email each time.

---

## What your email will look like

The digest email is organized in priority order:

**1. Tenders — Colombia** (most actionable for ARE)
  Each listing shows: title, source with link, organizer, deadline with days remaining,
  budget (if stated), a 1–2 sentence scope summary, strategic fit stars (★★★★★),
  and any risk flags (⚠ no budget, ⚠ local license required, etc.)

**2. Competitions — Colombia & Spain**

**3. Tenders — International**

**4. Competitions — International**

**⚠ Borderline section** (shown separately at the bottom)
  Items that passed the core filter but have complications — you decide.

---

## Costs breakdown

| Service | Cost |
|---|---|
| GitHub Actions | Free (2,000 minutes/month included) |
| SendGrid | Free (100 emails/day included) |
| Claude API (Sonnet 4.6) | ~$0.003 per 1K tokens. Expect $1–3/month for 2 runs/week |

Total: **under $5 USD/month** once your Anthropic credits are loaded.

---

## Troubleshooting

**"I got the email but it says 0 opportunities"**
This is normal on the first few runs while you tune the system. It can also mean
the websites changed their HTML structure. Check the log in Actions → your run → artifacts.

**"The workflow failed with a red X"**
Click on the failed run, click on the "monitor" job, expand the failed step.
The most common causes are: missing API key secret, or a website being temporarily down.

**"I want to add a new source"**
Edit `config/sources.py` and add your source following the same pattern as the others.
Commit the change through GitHub Desktop or the GitHub web editor.

**"I want to run it more or less often"**
Edit `.github/workflows/monitor.yml` and change the cron lines.
Cron format: `'0 12 * * 1'` = "at 12:00 UTC on Monday".
Use https://crontab.guru to generate cron expressions.

**"I want to change the filter logic"**
Edit `config/prompt.py`. The `SYSTEM_PROMPT` variable contains all the filter rules
in plain English — you can modify them directly.

---

## SECOP II — Important note

SECOP II data is fetched through Colombia's open data API (datos.gov.co),
which mirrors SECOP II procurement data publicly without requiring a login.
**Never share your SECOP II login with any system.**

The public API covers all published procurement processes. Your personal login
gives you access to draft/unpublished processes that we cannot and should not automate.

---

## Need help?

If something doesn't work, paste the error from the GitHub Actions log
into a conversation with Claude at claude.ai and it will help you debug it.
