from rest_framework import serializers
from ..models import SsOffice, SsStaff


class SsOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SsOffice
        fields = '__all__'


class SsStaffSerializer(serializers.ModelSerializer):
    office = SsOfficeSerializer(read_only=True)

    class Meta:
        model = SsStaff
        fields = ('id', 'staff_type','first_name', 'last_name', 'salutation',
                  'familiar_name', 'tel', 'tel_ext', 'email', 'office', 'notes',
                  'modified'
        )

