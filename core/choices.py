from django.db import models


class UserGender(models.TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"


class PurposeChoices(models.TextChoices):
    RESEARCH = "RESEARCH", "Research"
    PERSONAL_USE = "PERSONAL_USE", "Personal Use"
    INDUSTRIAL_USE = "INDUSTRIAL_USE", "Industrial Use"


class DemoRequestStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_REVIEW = "IN_REVIEW", "In Review"
    COMPLETED = "COMPLETED", "Completed"
