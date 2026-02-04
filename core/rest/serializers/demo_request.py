from rest_framework import serializers

from core.models import DemoRequest


class DemoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoRequest
        fields = "__all__"
