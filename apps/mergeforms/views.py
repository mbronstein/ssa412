# views
import json
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import Response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .serializers import  MergeFormSerializer
from django.conf import settings

from .models import MergeForm
# from tmdatamanager.tmdatamanager1 import TMDataManager

class MergeFormViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = MergeFormSerializer
    queryset = MergeForm.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


