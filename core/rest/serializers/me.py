from rest_framework import serializers

from core.models import User


class MeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "old_password",
            "is_otp_required",
        ]
        read_only_fields = ["email"]

    def validate_email(self, data):
        email = data.lower()
        user = self.instance

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise serializers.ValidationError("User with email already exists!")
        return email

    def validate(self, attrs):
        password = attrs.get("password")
        old_password = attrs.get("old_password")
        if password:
            if not old_password:
                raise serializers.ValidationError(
                    {"old_password": "Old password is required to set a new password."}
                )

            if not self.instance.check_password(old_password):
                raise serializers.ValidationError(
                    {"old_password": "Old password is incorrect."}
                )

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("old_password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
