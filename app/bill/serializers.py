from rest_framework import serializers

from core.models import Committee, Bill, Billview, Subscribe, Bookmark


class CommitteeSerializer(serializers.ModelSerializer):
    """Serializer for committee object"""
    bills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Bill.objects.all()
    )

    class Meta:
        model = Committee
        fields = ('id', 'committee', 'bills')
        read_only_Fields = ('id', )


class BillSerializer(serializers.ModelSerializer):
    """Serializer for bill object"""

    class Meta:
        model = Bill
        fields = ('id', 'bill', 'committee_id', 'count', 'lastupdated')
        read_only_Fields = ('id', )


class BillViewSerializer(serializers.ModelSerializer):
    """Serializer for billview object"""

    class Meta:
        model = Billview
        fields = '__all__'
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        alternative = []
        if ret['status']=='ALT':
            DL = Billview.objects.get(billno=ret['billno']).billviews.all()
            DL = [x['billno'] for x in list(DL.values('billno'))]
            ret['alternative'] = DL
        return ret


class BillViewCoverSerializer(serializers.ModelSerializer):
    """Serializer for billview object"""

    class Meta:
        model = Billview
        fields = ('billno', 'billname', 'billlink', 'generalresult', 'billstep',
                  'proposerdt', 'submitdt', 'procdt', 'finished', 'committee_id')
        read_only_Fields = ('id',)


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscribe object"""

    class Meta:
        model = Subscribe
        fields = ('id', 'subscribe_bill')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subscribe_bill'] = BillSerializer(
            Bill.objects.get(id=ret['subscribe_bill'])
        ).data
        return ret


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for bookmark object"""

    class Meta:
        model = Bookmark
        fields = ('id', 'bookmark')
        read_only_Fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['bookmark'] = BillViewSerializer(
            Billview.objects.get(billno=ret['bookmark'])
        ).data
        return ret
