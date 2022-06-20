from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ..models import Matter
from .serializers import MatterSerializer


class MatterViewSet(ModelViewSet):
    serializer_class = MatterSerializer
    queryset = Matter.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
