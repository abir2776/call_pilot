from django.db import models


class FeatureType(models.TextChoices):
    AI_CALL = "AI_CALL", "AI Call"
