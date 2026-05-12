from django.urls import path, include

urlpatterns = [
    path("bot/", include("bot.urls")),
]
