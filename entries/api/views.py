from ..models import Entry

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import EntrySerializer


class EntryViewSet(ModelViewSet):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()
    # lookup_field = "username"

    # def get_queryset(self, *args, **kwargs):
    #     return self.queryset.filter(id=self.request.user.id)
    #
    # @action(detail=False, methods=["GET"])
    # def me(self, request):
    #     serializer = UserSerializer(request.user, context={"request": request})
    #     return Response(status=status.HTTP_200_OK, data=serializer.data)
