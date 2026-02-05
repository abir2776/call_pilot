from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from contacts.models import Contacts


class ContactSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(required=False, allow_null=True)

    class Meta:
        model = Contacts
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "source",
            "origin",
            "status",
        ]


class ContactExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
