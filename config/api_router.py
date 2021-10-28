from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ssa412.users.api.views import UserViewSet
from ssoffices.api.views import SsOfficeViewSet, SsStaffViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("ssoffices", SsOfficeViewSet)
router.register("ssstaff", SsStaffViewSet)

app_name = "api"
urlpatterns = router.urls
