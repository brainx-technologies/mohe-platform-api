from django.conf import settings
from rest_framework import serializers

from mohe.measurement.models import Measurement, Asset
from mohe.patient.models import Patient


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'measurement', 'file')


class MeasurementSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Measurement
        fields = ('id', 'reference', 'patient',
                  'measurement_date', 'sync_date',
                  'raw_data', 'result', 'kplex', 'batch', 'status', 'lat', 'lng',
                  'device', 'device_timestamp', 'device_voltage', 'device_firmware_version',
                  'url')

    def get_url(self, obj):
        return f'https://app.{settings.MOHE_DOMAIN}/result/{obj.reference}/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(user=self.context['request'].user)

class WriteMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'reference', 'patient', 'measurement_date', 'sync_date',
                  'raw_data', 'result', 'kplex', 'batch',
                  'lat', 'lng',
                  'device', 'device_timestamp', 'device_voltage', 'device_firmware_version',
                  'app_platform', 'app_os_version', 'app_build_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(user=self.context['request'].user)


class UpdateMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'patient')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(user=self.context['request'].user)
