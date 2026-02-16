from rest_framework.generics import RetrieveUpdateAPIView

from core.rest.serializers.me import MeSerializer


class MeProfileView(RetrieveUpdateAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
