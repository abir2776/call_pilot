from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.choices import Status
from organizations.models import OrganizationPlatform


class Contacts(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Phone Number", blank=True, null=True
    )
    email = models.EmailField(unique=True)
    source = models.ForeignKey(
        OrganizationPlatform, on_delete=models.SET_NULL, null=True, blank=True
    )
    origin = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return f"{self.phone}-{self.origin}-{self.status}"
