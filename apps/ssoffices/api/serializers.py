from rest_framework import serializers
from utility.eager import EagerLoadingMixin
from ..models import SsOffice, SsStaff


class SsOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SsOffice
        fields = '__all__'


class SsStaffSerializer(serializers.ModelSerializer,EagerLoadingMixin):
    ssoffice = SsOfficeSerializer(many=False, read_only=False)
    select_related_fields = ('ssoffice',)
    prefetch_related_fields = ()

    class Meta:
        model = SsStaff
        fields = ('id', 'type', 'first_name', 'last_name', 'salutation',
                  'tel', 'tel_ext', 'personal_fax','email', 'ssoffice', 'notes', 'modified'
                  )

