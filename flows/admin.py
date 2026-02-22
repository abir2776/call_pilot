from django.contrib import admin

from .models import PreBuildFlow, OrganizationFlowConnection

admin.site.register(PreBuildFlow)
admin.site.register(OrganizationFlowConnection)
