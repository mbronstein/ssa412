from rest_framework.viewsets import ModelViewSet
from apps.ssoffices.models import SsOffice, SsStaff


from apps.ssoffices.api.serializers import SsOfficeSerializer, SsStaffSerializer

class SsOfficeViewSet(ModelViewSet):
    serializer_class = SsOfficeSerializer
    queryset = SsOffice.objects.all()
    filterset_fields = ['city', 'state', 'type']


class SsStaffViewSet(ModelViewSet):
    serializer_class = SsStaffSerializer
    filterset_fields = ['last_name', 'first_name','type','city', 'state' ]

    def get_queryset(self):
        queryset = SsStaff.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)
