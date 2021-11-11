from .views import EntryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'entries', EntryViewSet)
urlpatterns = router.urls
