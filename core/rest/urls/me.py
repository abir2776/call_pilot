from django.urls import path

from core.rest.views.me import MeProfileView

urlpatterns = [path("", MeProfileView.as_view(), name="me-profile")]
