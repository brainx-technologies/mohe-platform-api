from rest_framework import serializers

from mohe.kplex.models import Kplex


class KplexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kplex
        fields = ('id', 'name', 'acronym')
