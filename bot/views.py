from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from bot.services.x_poster import post_tweet
from bot.services.token_store import (
    get_pending_approval,
    delete_pending_approval,
    set_last_posted_video_id,
)


class ApprovalViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"], url_path="approve/(?P<pending_id>[^/.]+)")
    def approve(self, _request, pending_id: str):
        entry = get_pending_approval(pending_id)
        if not entry:
            return Response("Invalid or expired approval link.", status=status.HTTP_404_NOT_FOUND)

        post_tweet(entry["tweet_text"])
        set_last_posted_video_id(entry["video_id"])
        delete_pending_approval(pending_id)

        return Response(f"Tweet posted successfully!\n\n{entry['tweet_text']}")

    @action(detail=False, methods=["get"], url_path="reject/(?P<pending_id>[^/.]+)")
    def reject(self, _request, pending_id: str):
        entry = get_pending_approval(pending_id)
        if not entry:
            return Response("Invalid or expired approval link.", status=status.HTTP_404_NOT_FOUND)

        delete_pending_approval(pending_id)

        return Response(f"Tweet rejected for: {entry['video_title']}")

    @action(detail=False, methods=["get"])
    def health(self, _request):
        return Response({"status": "ok"})
