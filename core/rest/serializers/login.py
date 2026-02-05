# core/serializers.py (or authentication/serializers.py)
from rest_framework import serializers

from core.models import OTPToken


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)


class OTPVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        otp_code = attrs.get("otp_code")
        try:
            otp_token = OTPToken.objects.filter(
                otp_code=otp_code, is_used=False
            ).latest("created_at")
        except OTPToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP")

        if not otp_token.is_valid():
            raise serializers.ValidationError("Invalid or expired OTP")
        attrs["otp_token"] = otp_token
        return attrs
