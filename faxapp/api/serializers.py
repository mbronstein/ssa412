from rest_framework import serializers
from ..models import OutgoingFax


class OutgoingFaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingFax
        fields = '__all__'

