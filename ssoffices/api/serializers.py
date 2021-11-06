from rest_framework import serializers
from ..models import SsOffice, SsStaff


class SsOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SsOffice
        fields = '__all__'


class SsStaffSerializer(serializers.ModelSerializer):
    ssoffice = SsOfficeSerializer(read_only=False)

    class Meta:
        model = SsStaff
        fields = ('id', 'type', 'first_name', 'last_name', 'salutation',
                  'honorific', 'tel', 'tel_ext', 'email', 'ssoffice',
                  'notes', 'modified'
                  )

