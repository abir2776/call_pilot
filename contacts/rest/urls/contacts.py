from django.urls import path

from contacts.rest.views.contacts import (
    ContactListCreateAPIView,
    ContactExcelUploadAPIView,
)

urlpatterns = [
    path("", ContactListCreateAPIView.as_view(), name="contact-list-create"),
    path(
        "upload-excel",
        ContactExcelUploadAPIView.as_view(),
        name="contact-excel-upload",
    ),
]
