import pandas as pd
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contacts.models import Contacts
from contacts.rest.serializers.contacts import (
    ContactExcelUploadSerializer,
    ContactSerializer,
)


class ContactListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


class ContactExcelUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ContactExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        try:
            df = pd.read_excel(file)
        except Exception:
            return Response(
                {"error": "Invalid Excel file"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        required_columns = {"first_name", "last_name", "email", "phone"}
        if not required_columns.issubset(df.columns):
            return Response(
                {"error": f"Excel must contain columns: {', '.join(required_columns)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created = 0
        skipped = []

        for _, row in df.iterrows():
            email = str(row["email"]).strip()

            if Contacts.objects.filter(email=email).exists():
                skipped.append(email)
                continue

            Contacts.objects.create(
                first_name=str(row["first_name"]).strip(),
                last_name=str(row["last_name"]).strip(),
                email=email,
                phone=row["phone"] if pd.notna(row["phone"]) else None,
            )
            created += 1

        return Response(
            {
                "created": created,
                "skipped_duplicates": skipped,
            },
            status=status.HTTP_201_CREATED,
        )
