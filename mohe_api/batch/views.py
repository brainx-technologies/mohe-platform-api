from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mohe.kplex.models import Batch
from mohe_api.batch.serializers import BatchSerializer


class BatchViewSet(ReadOnlyModelViewSet):
    """
    Read only api for biomarkers.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
