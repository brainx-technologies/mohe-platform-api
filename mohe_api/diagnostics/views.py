from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mohe.diagnostics.models import Biomarker, Category
from mohe_api.diagnostics.serializers import BiomarkerSerializer, CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BioMarkerViewSet(ReadOnlyModelViewSet):
    """
    Read only api for biomarkers.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BiomarkerSerializer
    queryset = Biomarker.objects.all()
