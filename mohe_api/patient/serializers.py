from rest_framework import serializers

from mohe.patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'birthday', 'sex', 'comment', 'photo')
