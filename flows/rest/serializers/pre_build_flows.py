from rest_framework import serializers

from flows.models import OrganizationFlowConnection, PreBuildFlow


class PreBuildFlowSerializer(serializers.ModelSerializer):
    is_connected = serializers.SerializerMethodField()

    class Meta:
        model = PreBuildFlow
        fields = "__all__"

    def get_is_connected(self, obj):
        organization = self.context["request"].user
        return OrganizationFlowConnection.objects.filter(
            organization=organization, flow=obj
        ).exists()


class MyFlowsSerializer(serializers.ModelSerializer):
    flow = PreBuildFlowSerializer()

    class Meta:
        model = OrganizationFlowConnection
        fields = "__all__"
