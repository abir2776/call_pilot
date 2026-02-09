import logging
import random
import string
import uuid

from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from versatileimagefield.fields import VersatileImageField

from common.choices import Status
from common.models import BaseModelWithUID

from .choices import DemoRequestStatus, PurposeChoices, UserGender
from .managers import CustomUserManager
from .utils import get_user_media_path_prefix, get_user_slug

logger = logging.getLogger(__name__)


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True, editable=False)
    phone = PhoneNumberField(
        unique=True, db_index=True, verbose_name="Phone Number", blank=True, null=True
    )
    slug = AutoSlugField(populate_from=get_user_slug, unique=True)
    avatar = VersatileImageField(
        "Avatar",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    image = VersatileImageField(
        "Image",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.UNKNOWN,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    token = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"UID: {self.uid}, Phone: {self.phone}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def get_organization(self):
        return (
            self.organization_profile.filter(is_active=True)
            .select_related("organization")
            .first()
            .organization
        )

    def get_role(self):
        return self.organization_profile.filter(is_active=True).first().role


class DemoRequest(BaseModelWithUID):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = PhoneNumberField()
    purpose = models.CharField(max_length=20, choices=PurposeChoices.choices)
    company_category = models.CharField(max_length=255, null=True, blank=True)
    employee_size = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=DemoRequestStatus.choices,
        default=DemoRequestStatus.PENDING,
    )

    def __str__(self):
        return f"{self.email}-{self.purpose}"


class OTPToken(BaseModelWithUID):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    remember_me = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at

    @staticmethod
    def generate_otp():
        return "".join(random.choices(string.digits, k=6))

    def __str__(self):
        return f"OTP for {self.user.email} - {self.otp_code}"
