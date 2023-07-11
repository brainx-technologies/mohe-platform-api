from rest_framework import serializers

from mohe.measurement.models import Measurement
from mohe.patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    result_count = serializers.SerializerMethodField()

    def get_result_count(self, obj):
        return Measurement.objects.filter(patient=obj).count()

    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'birthday', 'sex', 'comment', 'photo', 'result_count')
