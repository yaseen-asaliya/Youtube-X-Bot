import anthropic
import os
import re

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_tweet_draft(title: str, description: str, video_url: str) -> str:
    desc_snippet = description[:400] if description else "(no description)"

    prompt = f"""You are a social-media copywriter. Write a single punchy X (Twitter) post to promote a new YouTube video.

Video title: {title}
Video description: {desc_snippet}
Video URL: {video_url}

Hard rules — violating any of these makes the output unusable:
1. Total length including the URL must be 280 characters or fewer.
2. Use at most 2 hashtags.
3. The tweet must end with exactly this URL on its own: {video_url}
4. Output of the tweet must have a breife summary of the video.
5. The tweet must have the last line as "Video out now on my YouTube channel!"

Write the tweet now:"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    tweet = message.content[0].text.strip()

    if not tweet:
        raise ValueError("Claude returned an empty response")

    # Safety net: ensure the URL is at the end
    if not tweet.endswith(video_url):
        tweet = re.sub(r'https?://\S+$', '', tweet).rstrip() + ' ' + video_url

    # Safety net: enforce 280-char hard limit
    if len(tweet) > 280:
        max_body = 280 - len(video_url) - 1
        body = tweet[:len(tweet) - len(video_url) - 1]
        tweet = body[:max_body].rstrip() + ' ' + video_url

    # Safety net: strip excess hashtags (keep first 2)
    tags = re.findall(r'#\w+', tweet)
    if len(tags) > 2:
        keep = set(tags[:2])
        seen = {}
        def _replace(m):
            tag = m.group(0)
            seen[tag] = seen.get(tag, 0) + 1
            if tag not in keep:
                return ''
            return tag
        tweet = re.sub(r'#\w+', _replace, tweet)
        tweet = re.sub(r' {2,}', ' ', tweet).strip()
        if not tweet.endswith(video_url):
            tweet = re.sub(r'https?://\S+$', '', tweet).rstrip() + ' ' + video_url

    print(f"Tweet draft generated ({len(tweet)}/280 chars)")
    return tweet
