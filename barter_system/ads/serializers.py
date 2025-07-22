from rest_framework import serializers
from .models import Ad, ExchangeProposal


class AdSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'

class ExchangeProposalSerializer(serializers.ModelSerializer):
    ad_sender = AdSerializer(read_only=True)
    ad_receiver = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = '__all__'
