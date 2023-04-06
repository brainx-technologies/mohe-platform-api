from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from mohe.kplex.models import Parameter
from mohe_api.parameter.serializers import ParameterSerializer


class ParameterViewSet(ReadOnlyModelViewSet):
    """
    Read only api for biomarkers.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ParameterSerializer
    queryset = Parameter.objects.all()
