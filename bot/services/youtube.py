import feedparser

YOUTUBE_RSS_BASE = "https://www.youtube.com/feeds/videos.xml?channel_id="


def get_latest_video(channel_id: str) -> dict | None:
    feed = feedparser.parse(YOUTUBE_RSS_BASE + channel_id)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    return {
        "id": entry.get("yt_videoid", ""),
        "title": entry.get("title", ""),
        "url": entry.get("link", ""),
        "description": entry.get("summary", ""),
        "published": entry.get("published", ""),
    }
