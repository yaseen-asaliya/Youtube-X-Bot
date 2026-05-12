from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from bot.models import PendingApproval
from services.x_poster import post_tweet
from services.token_store import set_last_posted_video_id


@require_GET
def approve(request, pending_id: str):
    try:
        entry = PendingApproval.objects.get(pending_id=pending_id)
    except PendingApproval.DoesNotExist:
        return HttpResponse("Invalid or expired approval link.", status=404)

    post_tweet(entry.tweet_text)
    set_last_posted_video_id(entry.video_id)
    entry.delete()

    return HttpResponse(
        f"Tweet posted successfully!\n\n{entry.tweet_text}",
        content_type="text/plain",
    )


@require_GET
def reject(request, pending_id: str):
    try:
        entry = PendingApproval.objects.get(pending_id=pending_id)
    except PendingApproval.DoesNotExist:
        return HttpResponse("Invalid or expired approval link.", status=404)

    title = entry.video_title
    entry.delete()

    return HttpResponse(
        f"Tweet rejected for: {title}",
        content_type="text/plain",
    )


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})
