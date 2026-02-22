from django.urls import path

from flows.rest.views.pre_build_flows import (
    ConnectFlowOrganizationAPIView,
    MyFlowsList,
    PrebuildFlowListAPIView,
)

urlpatterns = [
    path("", PrebuildFlowListAPIView.as_view(), name="available-flow-list"),
    path(
        "<uuid:flow_uid>/connect",
        ConnectFlowOrganizationAPIView.as_view(),
        name="organization-flow-connect",
    ),
    path("my_flows", MyFlowsList.as_view(), name="my-flow-list"),
]
