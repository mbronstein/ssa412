from rest_framework import serializers
from ..models import SsOffice, SsStaff


class SsOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SsOffice
        fields = '__all__'


class SsStaffSerializer(serializers.ModelSerializer):
    ss_office = SsOfficeSerializer(read_only=True)
    class Meta:
        model = SsStaff
        fields = '__all__'
