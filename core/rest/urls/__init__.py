from django.urls import include, path

urlpatterns = [path("demo/", include("core.rest.urls.demo_request"))]
