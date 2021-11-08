from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from faxapp.models import OutgoingFax
from faxapp.api.serializers import OutgoingFaxSerializer

@api_view(['POST', ])
def send_fax(request):
    serializer = OutgoingFaxSerializer(data=request.data)
    serializer.save()
    return Response(serializer.data)
