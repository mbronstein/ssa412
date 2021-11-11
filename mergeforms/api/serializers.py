from rest_framework import serializers
from ..models import MergeForm


class MergeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MergeForm
        fields = '__all__'

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }
