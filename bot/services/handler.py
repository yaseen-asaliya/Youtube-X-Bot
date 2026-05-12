import os
import uuid
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_x_bot.settings")
django.setup()

from bot.services.youtube import get_latest_video
from bot.services.ai import generate_tweet_draft
from bot.services.notify import send_approval_email
from bot.services.token_store import get_last_posted_video_id
from bot.models import PendingApproval


def lambda_handler(event: dict, context) -> dict:
    channel_id = os.environ["YOUTUBE_CHANNEL_ID"]

    video = get_latest_video(channel_id)
    if not video:
        print("No videos found in RSS feed")
        return {"statusCode": 200, "body": "No videos found"}

    last_id = get_last_posted_video_id()
    if video["id"] == last_id:
        print(f"No new video (last posted: {last_id})")
        return {"statusCode": 200, "body": "No new video"}

    print(f"New video found: {video['title']}")

    tweet = generate_tweet_draft(video["title"], video["description"], video["url"])
    print(f"Generated tweet:\n{tweet}")

    pending_id = str(uuid.uuid4())
    PendingApproval.objects.create(
        pending_id=pending_id,
        video_id=video["id"],
        video_title=video["title"],
        video_url=video["url"],
        tweet_text=tweet,
    )

    send_approval_email(video, tweet, pending_id)

    return {"statusCode": 200, "body": f"Approval email sent for: {video['title']}"}
