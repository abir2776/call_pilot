from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from core.rest.views.login import LoginRequestView, OTPVerifyView

schema_view = get_schema_view(
    openapi.Info(
        title="call_pilot API",
        default_version="main",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger
    re_path(
        r"^docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=10),
        name="schema-json",
    ),
    re_path(
        r"^docs/swagger$",
        schema_view.with_ui("swagger", cache_timeout=10),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^docs/redoc$",
        schema_view.with_ui("redoc", cache_timeout=10),
        name="schema-redoc",
    ),
    # JWT Token
    path(
        "api/v1/token",
        LoginRequestView.as_view(),
        name="login_request",
    ),
    path(
        "api/v1/token/verify-otp",
        OTPVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("organizations.rest.urls.register")),
    path("api/v1/organizations/", include("organizations.rest.urls")),
    path("api/v1/core/", include("core.rest.urls")),
    path("api/v1/contacts/", include("contacts.rest.urls.contacts")),
    path("api/v1/phone_number/", include("phone_number.rest.urls.phone_numbers")),
    path("api/v1/interview/", include("interview.rest.urls")),
    path("api/v1/auth/organizations/", include("organizations.rest.urls.register")),
    path("api/v1/subscription/", include("subscription.rest.urls")),
    path("api/v1/me/", include("core.rest.urls.me")),
    path("api/v1/flows/", include("flows.rest.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
