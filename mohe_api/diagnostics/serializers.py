from rest_framework import serializers

from mohe.diagnostics.models import Biomarker, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class BiomarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biomarker
        fields = ('id', 'name', 'acronym', 'category')
