from django.urls import include, path

urlpatterns = [path("", include("contacts.rest.urls.contacts"))]
