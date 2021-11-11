from rest_framework.routers import SimpleRouter
from .views import MergeFormViewSet

router = SimpleRouter()
router.register("mergeforms", MergeFormViewSet)
urlpatterns = router.urls
