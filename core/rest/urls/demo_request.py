from django.urls import path

from core.rest.views.demo_request import DemoRequestListCreateAPIView

urlpatterns = [
    path(
        "requests",
        DemoRequestListCreateAPIView.as_view(),
        name="demo-request-list-create",
    )
]
