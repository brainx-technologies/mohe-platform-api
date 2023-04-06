from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from mohe_api.facility.serializers import FacilitySerializer


class FacilityViewSet(ViewSet):
    """
    This endpoint returns the user profile for the authenticated user.
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request, format=None):
        serializer = FacilitySerializer(request.user.facility)
        return Response(serializer.data)
