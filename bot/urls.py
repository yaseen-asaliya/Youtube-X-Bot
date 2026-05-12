from django.urls import path
from bot import views

urlpatterns = [
    path("approve/<str:pending_id>/", views.approve, name="approve"),
    path("reject/<str:pending_id>/", views.reject, name="reject"),
    path("health/", views.health, name="health"),
]
