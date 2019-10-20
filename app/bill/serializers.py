from rest_framework import serializers

from core.models import Bill, Billview, Subscribe


class BillSerializer(serializers.ModelSerializer):
    """Serializer for bill object"""

    class Meta:
        model = Bill
        fields = ('id', 'bill')
        read_only_Fields = ('id', 'bill',)


class BillDetailSerializer(serializers.ModelSerializer):
    """Serializer for subscribe object"""

    class Meta:
        model = Billview
        fields = '__all__'
        read_only_Fields = ('id',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscribe object"""

    class Meta:
        model = Subscribe
        fields = ('id', 'subscribe_bill')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subscribe_bill'] = {
            'bill_id': ret['subscribe_bill'],
            'bill_name':
            BillSerializer(
                Bill.objects.get(id=ret['subscribe_bill'])
            ).data['bill']
        }
        return ret
