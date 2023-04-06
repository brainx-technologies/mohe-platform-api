from rest_framework import serializers

from mohe.kplex.models import Parameter


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'biomarker', 'position', 'kplex')
