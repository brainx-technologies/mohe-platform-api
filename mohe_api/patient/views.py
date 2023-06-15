import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from mohe.patient.models import Patient
from mohe_api.patient import serializers

LOGGER = logging.getLogger(__name__)


class PatientViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
