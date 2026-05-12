from django.db import models


class PendingApproval(models.Model):
    pending_id = models.CharField(max_length=36, unique=True)
    video_id = models.CharField(max_length=50)
    video_title = models.TextField()
    video_url = models.URLField()
    tweet_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.video_title[:60]} ({self.pending_id[:8]})"
