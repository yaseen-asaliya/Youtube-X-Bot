# API Reference

All external APIs used in this project.

---

## 1. Anthropic Claude

**File:** `services/ai.py` | **SDK:** `anthropic` | **Env var:** `ANTHROPIC_API_KEY`

Generates tweet drafts from a video title, description, and URL.

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    messages=[{"role": "user", "content": prompt}],
)
# returns: message.content[0].text
```

**Prompt rules enforced:**
1. Total length ≤ 280 characters (including URL)
2. At most 2 hashtags
3. Tweet must end with the video URL
4. Must include a brief video summary
5. Last line: `"Video out now on my YouTube channel!"`

**Post-generation safety nets applied in code:**

| Check | Action |
|-------|--------|
| Empty response | Raise `ValueError` |
| URL not at end | Strip trailing URL, re-append `video_url` |
| Length > 280 chars | Truncate body, re-append `video_url` |
| More than 2 hashtags | Remove excess, collapse spaces |

Get a key: <https://console.anthropic.com/settings/keys>

---

## 2. Twitter / X API

**File:** `services/x_poster.py` | **SDK:** `tweepy` | **API version:** v2

Posts a tweet on behalf of the authenticated account.

```python
tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
).create_tweet(text=tweet_text)
```

**Required env vars:**

| Variable | Description |
|----------|-------------|
| `TWITTER_API_KEY` | OAuth 1.0a consumer key |
| `TWITTER_API_SECRET` | OAuth 1.0a consumer secret |
| `TWITTER_ACCESS_TOKEN` | Access token for the posting account |
| `TWITTER_ACCESS_TOKEN_SECRET` | Access token secret |

App must have **Read and Write** permissions. OAuth 1.0a User Context required.  
Get credentials: <https://developer.twitter.com/en/portal/dashboard>

---

## 3. YouTube RSS Feed

**File:** `services/youtube.py` | **Library:** `feedparser` | **No API key required**

Polls the public RSS feed for a channel's latest video.

```
GET https://www.youtube.com/feeds/videos.xml?channel_id=<YOUTUBE_CHANNEL_ID>
```

Returns:
```python
{ "id": "dQw4w9WgXcQ", "title": "...", "url": "...", "description": "...", "published": "..." }
```

The returned `id` is compared against the last posted ID in SSM to avoid duplicates.  
Find your channel ID at: <https://commentpicker.com/youtube-channel-id.php>

---

## 4. Amazon SES

**File:** `services/notify.py` | **SDK:** `boto3` | **AWS API:** `ses:SendEmail`

Sends a plain-text approval email with one-click approve/reject links.

```python
ses.send_email(
    Source=SES_SENDER_EMAIL,
    Destination={"ToAddresses": [SES_APPROVER_EMAIL]},
    Message={"Subject": {...}, "Body": {"Text": {...}}},
)
```

**Required env vars:**

| Variable | Description |
|----------|-------------|
| `SES_SENDER_EMAIL` | Verified sender address |
| `SES_APPROVER_EMAIL` | Recipient for approval emails |
| `APPROVAL_BASE_URL` | Base URL for approve/reject links |

New AWS accounts are in **sandbox mode** — both sender and recipient must be verified.  
Verify an address: `aws ses verify-email-identity --email-address you@example.com`

**IAM policy required:**
```json
{ "Effect": "Allow", "Action": "ses:SendEmail", "Resource": "*" }
```

---

## 5. AWS SSM Parameter Store

**File:** `services/token_store.py` | **SDK:** `boto3` | **AWS APIs:** `ssm:GetParameter`, `ssm:PutParameter`

Stores persistent state (last posted video ID) across Lambda invocations.

| Parameter | Type | Purpose |
|-----------|------|---------|
| `/youtube-x-bot/last_video_id` | `String` | ID of the last video posted to X |

```python
get_last_posted_video_id() -> str | None
set_last_posted_video_id(video_id: str) -> None
```

**IAM policy required:**
```json
{
  "Effect": "Allow",
  "Action": ["ssm:GetParameter", "ssm:PutParameter"],
  "Resource": "arn:aws:ssm:<region>:<account-id>:parameter/youtube-x-bot/*"
}
```
