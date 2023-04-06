from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mohe.diagnostics.models import Biomarker
from mohe_api.diagnostics.serializers import BiomarkerSerializer


class BioMarkerViewSet(ReadOnlyModelViewSet):
    """
    Read only api for biomarkers.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BiomarkerSerializer
    queryset = Biomarker.objects.all()
