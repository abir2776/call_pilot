from django.urls import path

from ..views import organization_platform

urlpatterns = [
    path(
        "",
        organization_platform.PlatformListView.as_view(),
        name="organization-platform-list",
    ),
    path(
        "connect",
        organization_platform.ConnectPlatformView.as_view(),
        name="organization-platform-connect",
    ),
    path(
        "my_platforms",
        organization_platform.MyPlatformListView.as_view(),
        name="my_platforms_list",
    ),
    path(
        "my_platforms/<uuid:uid>",
        organization_platform.MyPlatformDetailsView.as_view(),
        name="my_platforms_list",
    ),
]
