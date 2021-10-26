from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ssoffices.models import SsOffice, SsStaff


from ssoffices.api.serializers import SsOfficeSerializer, SsStaffSerializer

class SsOfficeViewSet(ModelViewSet):
    serializer_class = SsOfficeSerializer
    queryset = SsOffice.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', 'type']


class SsStaffViewSet(ModelViewSet):
    serializer_class = SsStaffSerializer
    queryset = SsStaff.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name']
