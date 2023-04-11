from rest_framework import serializers
from mohe.hardware.models import Model, Device, Firmware


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'key', 'name', 'bootloader', 'status', 'hex')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'model', 'hardware_key', 'serial_number', 'status')


class FirmwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firmware
        fields = ('id', 'model', 'version_name', 'version_number', 'status', 'release_notes', 'file', 'checksum', 'hex',
                  'date')
