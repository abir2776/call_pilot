from django.contrib import admin

from organizations.models import (
    Organization,
    OrganizationPlatform,
    OrganizationUser,
    OrganizationUserInvitation,
    Platform,
)

admin.site.register(Organization)
admin.site.register(OrganizationPlatform)
admin.site.register(Platform)
admin.site.register(OrganizationUserInvitation)
admin.site.register(OrganizationUser)
