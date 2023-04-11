from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from mohe.hardware.models import Device, Model, Firmware
from .serializers import DeviceSerializer, ModelSerializer, FirmwareSerializer


class ModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = (IsAuthenticated,)


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAuthenticated,)


class FirmwareViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Firmware.objects.all()
    serializer_class = FirmwareSerializer
    permission_classes = (IsAuthenticated,)
