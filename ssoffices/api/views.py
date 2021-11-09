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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'last_name', 'type' ]

    def get_queryset(self):
        queryset = SsStaff.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)
