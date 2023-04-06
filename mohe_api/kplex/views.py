from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mohe.kplex.models import Kplex
from mohe_api.kplex.serializers import KplexSerializer


class KplexViewSet(ReadOnlyModelViewSet):
    """
    Read only api for biomarkers.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = KplexSerializer
    queryset = Kplex.objects.all()
