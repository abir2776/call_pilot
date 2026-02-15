from django.contrib import admin

from core.models import DemoRequest, OTPToken, User

admin.site.register(User)
admin.site.register(OTPToken)
admin.site.register(DemoRequest)
