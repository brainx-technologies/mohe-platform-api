from rest_framework import serializers

from mohe.kplex.models import Batch


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ('id', 'kplex', 'barcode', 'batch_number', 'production_date', 'expiry_date', 'status')
