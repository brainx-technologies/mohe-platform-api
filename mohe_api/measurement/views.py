import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from mohe.measurement.models import Measurement, Asset
from mohe_api.measurement import serializers

LOGGER = logging.getLogger(__name__)


class AssetViewset(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer

    def get_queryset(self):
        return Asset.objects.filter(measurement__user=self.request.user)

    def perform_create(self, serializer):
        measurement = get_object_or_404(Measurement, user=self.request.user)
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
        # TODO: generally log error response bodies, remove this method
        try:
            result = super(MeasurementViewSet, self).dispatch(request, *args, **kwargs)
        except Exception as e:
            LOGGER.exception("an error occured")
            raise e

        return result

    def create(self, request, *args, **kwargs):
        # TODO: remove (HACK for logging)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

        try:
            obj = serializer.save(user=user)
            obj.save()
        except Exception as e:
            raise ValidationError({'save': ['error saving object: "{0}"'.format(e)]})
