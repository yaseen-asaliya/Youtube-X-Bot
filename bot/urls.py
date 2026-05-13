from rest_framework.routers import DefaultRouter
from bot.views import ApprovalViewSet

router = DefaultRouter()
router.register(r"", ApprovalViewSet, basename="approval")

urlpatterns = router.urls
