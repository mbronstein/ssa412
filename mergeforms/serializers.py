from rest_framework import serializers
from .models import MergeForm


class MergeFormListSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    filepath = serializers.ReadOnlyField()

    class Meta:
        model = MergeForm
        fields = '__all__'


class MergeFormSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    filepath = serializers.ReadOnlyField()

    class Meta:
        model = MergeForm
        fields = '__all__'
