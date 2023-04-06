from rest_framework import serializers

from mohe.diagnostics.models import Biomarker


class BiomarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biomarker
        fields = ('id', 'name', 'acronym')
