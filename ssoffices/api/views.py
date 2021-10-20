from ssoffices.models import SsOffice, SsStaff
from rest_framework.viewsets import ModelViewSet

from ssoffices.api.serializers import SsOfficeSerializer, SsStaffSerializer

class SsOfficeViewSet(ModelViewSet):
    serializer_class = SsOfficeSerializer
    queryset = SsOffice.objects.all()


class SsStaffViewSet(ModelViewSet):
    serializer_class = SsStaffSerializer
    queryset = SsStaff.objects.all()
