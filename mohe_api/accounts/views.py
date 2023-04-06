from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from mohe_api.accounts.serializers import UserSerializer


class UserViewSet(ViewSet):
    """
    This endpoint returns the user profile for the authenticated user.
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
