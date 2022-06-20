from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from mergeforms.serializers import MergeFormListSerializer, MergeFormSerializer
from mergeforms.models import MergeForm


# from todoapp.contacts.models import Contact




class MergeFormListCreateView(ListCreateAPIView):
    """get list of forms """
    serializer_class = MergeFormListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = MergeForm.objects.all()
    filter_fields = ()
[]


class MergeFormRetrieveView(RetrieveAPIView):
    """used to retrieve a form (get) or render a form with a context (put)"""
    serializer_class = MergeFormSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
    queryset = MergeForm.objects.all()
