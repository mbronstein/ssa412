from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ssa412.users.api.views import UserViewSet
from ssoffices.api.views import SsOfficeViewSet, SsStaffViewSet
from matters.api.views import MatterViewSet
# from faxapp.api.views import OutgoingFaxViewSet)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("ssoffices", SsOfficeViewSet)
router.register("ssstaff", SsStaffViewSet, basename="ssstaff")
# above basename param had to be added for LazyMixin and get_query
router.register("matters", MatterViewSet)
# router.register("fax", OutgoingFaxViewSet)

app_name = "api"
urlpatterns = router.urls
