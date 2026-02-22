from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.choices import Status
from organizations.models import Organization
from common.models import BaseModelWithUID


class PreBuildFlow(BaseModelWithUID):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    features = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    code = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return f"Title: {self.title}, Status: {self.status}"


class OrganizationFlowConnection(BaseModelWithUID):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    flow = models.ForeignKey(PreBuildFlow, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        unique_together = ["organization", "flow"]

    def __str__(self):
        return f"{self.organization.name} - {self.flow.title}"
