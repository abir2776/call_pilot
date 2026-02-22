from django.urls import include, path

urlpatterns = [path("available-flow/", include("flows.rest.urls.pre_build_flows"))]
