from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import DemoRequest
from core.rest.serializers.demo_request import DemoRequestSerializer


class DemoRequestListCreateAPIView(ListCreateAPIView):
    serializer_class = DemoRequestSerializer
    queryset = DemoRequest.objects.filter()

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]
