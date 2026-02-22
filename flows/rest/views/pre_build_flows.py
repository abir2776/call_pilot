from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from flows.models import OrganizationFlowConnection, PreBuildFlow
from flows.rest.serializers.pre_build_flows import (
    MyFlowsSerializer,
    PreBuildFlowSerializer,
)


class PrebuildFlowListAPIView(ListAPIView):
    serializer_class = PreBuildFlowSerializer
    queryset = PreBuildFlow.objects.filter()


class ConnectFlowOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, flow_uid):
        flow = get_object_or_404(PreBuildFlow, uid=flow_uid)

        organization = request.user.get_organization()

        if not organization:
            return Response(
                {"detail": "User does not belong to any organization."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        exists = OrganizationFlowConnection.objects.filter(
            flow=flow, organization=organization
        ).exists()
        if exists:
            return Response(
                {"detail": "Organization is already connected with this flow."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        OrganizationFlowConnection.objects.create(flow=flow, organization=organization)

        return Response(
            {
                "detail": "Flow successfully connected to organization.",
                "flow_uid": str(flow.uid),
                "organization_id": organization.id,
            },
            status=status.HTTP_200_OK,
        )


class MyFlowsList(ListAPIView):
    serializer_class = MyFlowsSerializer

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return OrganizationFlowConnection.objects.filter(organization=organization)
