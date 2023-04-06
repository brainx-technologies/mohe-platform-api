import json
import logging

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from mohe.measurement.models import Measurement, Asset, MeasurementField
from mohe_api.measurement import serializers

LOGGER = logging.getLogger(__name__)


class AssetViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer

    def get_queryset(self):
        measurement_id = self.kwargs.get('measurement')
        measurement = get_object_or_404(Measurement, pk=measurement_id, user=self.request.user)
        return Asset.objects.filter(measurement_id=measurement)

    def perform_create(self, serializer):
        measurement_id = self.kwargs.get('measurement')
        measurement = get_object_or_404(Measurement, pk=measurement_id, user=self.request.user)
        serializer.save(measurement=measurement)


class MeasurementViewSet(ModelViewSet):
    """
    Returns the list of all measurements made by the user.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MeasurementSerializer
    page_size = 10
    pagination_class = LimitOffsetPagination

    def initial(self, request, *args, **kwargs):
        super(MeasurementViewSet, self).initial(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            result = super(MeasurementViewSet, self).dispatch(request, *args, **kwargs)
            if result.status_code not in (200, 201):
                LOGGER.error("response: {} for {}".format(result.status_code, result.data))
        except Exception as e:
            LOGGER.exception("an error occured")
            raise e

        return result

    def get_queryset(self):
        return Measurement.objects.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action in ('list', 'detail'):
            return serializers.MeasurementSerializer
        elif self.action in ('update',):
            return serializers.UpdateMeasurementSerializer
        return serializers.WriteMeasurementSerializer

    def perform_create(self, serializer):
        user = self.request.user

        LOGGER.info("CREATE: " + json.dumps(serializer.initial_data, indent=4))

        # check if user has upload team
        if not user.team:
            raise ValidationError({"team": ['Default upload team not set. Please contact your administrator.']})

        try:
            obj = serializer.save(user=user, team=user.team)
            obj.save()
        except Exception as e:
            raise ValidationError({'save': ['error saving object: "{0}"'.format(e)]})


class MeasurementFieldViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MeasurementFieldSerializer
    queryset = MeasurementField.objects.all().order_by('position')
