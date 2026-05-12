# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Youtube-X-Bot is a serverless automation pipeline on AWS that monitors YouTube RSS feeds. Using Claude AI for content generation and Amazon SES for approval workflows, this project bridges automated content creation with social media publishing. It is designed to be architected, deployed, and tested through a step-by-step local and cloud-based integration guide.

## Architecture

The system has two entry points into Lambda:

- **EventBridge** fires `POST /check` on a ~10-minute schedule to poll the YouTube RSS feed for new videos.
- **API Gateway** routes approve/reject clicks from the approval email back to Lambda.

**Full data flow:**

1. EventBridge triggers `lambda_handler` → `youtube.py` fetches RSS feed
2. Latest video ID is compared against `last_video_id` stored in SSM — if identical, pipeline exits
3. `ai.py` calls Claude to generate a tweet draft
4. `notify.py` sends an approval email via SES containing the draft and two one-click URLs
5. User clicks **Approve** or **Reject** in their email client → hits API Gateway
6. On approve: `x_poster.py` posts the tweet to Twitter/X, SSM `last_video_id` is updated and the approval token is cleared
7. On reject: the pending approval record is deleted, nothing is posted

**SSM Parameter Store holds three things:**
- `last_video_id` — deduplication; prevents re-posting the same video
- approval token — scoped to one pending approval, validated on the approve/reject request
- token cleared after use

**Django's role** is limited to serving the approve/reject webhook endpoints (`bot/views.py`). The Lambda orchestration logic lives in `handler.py` and the `services/` package.

## Getting Started

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 2. Install dependencies
pip install -r bot/docs/requirements.txt

# 3. Copy and fill in environment variables
cp bot/docs/.env.example .env

# 4. Run Django migrations
python manage.py migrate

# 5. Trigger the pipeline once + start approval server locally
python -m bot.services.local_server
```

For local approve/reject testing, expose the Django server with [ngrok](https://ngrok.com) and set `APPROVAL_BASE_URL` to the ngrok URL.

## Deployment

```bash
bash deploy.sh   # installs deps, migrates, deploys to AWS Lambda via Zappa
```

## Project Structure

```
Youtube-X-Bot/
├── bot/                    ← Django app
│   ├── services/           ← all business logic
│   │   ├── handler.py      ← Lambda entry point
│   │   ├── local_server.py ← local dev runner
│   │   ├── ai.py           ← Claude tweet generation
│   │   ├── youtube.py      ← YouTube RSS polling
│   │   ├── x_poster.py     ← Twitter/X posting via Tweepy
│   │   ├── notify.py       ← Amazon SES approval email
│   │   └── token_store.py  ← AWS SSM Parameter Store
│   ├── docs/
│   │   ├── architecture.png  ← system architecture diagram
│   │   ├── api.md            ← API reference
│   │   ├── requirements.txt  ← Python dependencies
│   │   └── .env.example      ← environment variable template
│   ├── models.py           ← PendingApproval model
│   ├── views.py            ← approve / reject / health views
│   ├── urls.py
│   └── migrations/
├── youtube_x_bot/          ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py

├── deploy.sh

└── .gitignore
```