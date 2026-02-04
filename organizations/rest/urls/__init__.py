from django.urls import include, path

urlpatterns = [
    path("platform/", include("organizations.rest.urls.organization_platform")),
]
