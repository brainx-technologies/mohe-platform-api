from rest_framework import serializers

from mohe.measurement.models import Measurement, Asset, MeasurementField


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'file')


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            'id', 'reference', 'title', 'comment', 'age', 'gender', 'extra_fields', 'measurement_date', 'sync_date',
            'raw_data', 'result', 'status', 'lat', 'lng', 'team',
            'device', 'device_timestamp', 'device_voltage', 'device_firmware_version',
            'kplex', 'batch', 'assets')


class WriteMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'reference', 'title', 'comment', 'age', 'gender', 'extra_fields', 'measurement_date', 'sync_date', 'raw_data', 'result',
                  'lat', 'lng', 'device', 'device_timestamp', 'device_voltage', 'device_firmware_version',
                  'kplex', 'batch', 'app_platform', 'app_os_version', 'app_build_number')


class UpdateMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'reference', 'title', 'comment', 'age', 'gender', 'extra_fields')


class MeasurementFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementField
        fields = ('id', 'name', 'kind', 'label', 'help_text', 'position')