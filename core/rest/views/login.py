from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from common.tasks import send_email_task
from core.models import OTPToken, User
from core.rest.serializers.login import LoginRequestSerializer, OTPVerifySerializer


class LoginRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].lower()
        password = serializer.validated_data["password"]
        remember_me = serializer.validated_data["remember_me"]

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_otp_required:
            otp_code = OTPToken.generate_otp()

            OTPToken.objects.create(
                email=email,
                otp_code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=10),
                remember_me=remember_me,
            )

            context = {
                "user_name": email,
                "otp_code": otp_code,
                "valid_minutes": 10,
            }

            send_email_task.delay(
                subject="Your Login OTP Code",
                recipient=email,
                template_name="emails/otp_login.html",
                context=context,
            )

            return Response(
                {
                    "message": "OTP sent to your email",
                    "email": email,
                    "otp_required": True,
                },
                status=status.HTTP_200_OK,
            )
        refresh = RefreshToken.for_user(user)
        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))

        return Response(
            {
                "otp_required": False,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class OTPVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_token = serializer.validated_data["otp_token"]
        user = User.objects.filter(email=otp_token.email).first()

        otp_token.is_used = True
        otp_token.save()
        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(days=1))
        if otp_token.remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(days=1))

        return Response(
            {
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {"id": user.id, "email": user.email},
            },
            status=status.HTTP_200_OK,
        )
