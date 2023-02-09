from .models import Collection
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'volume_24h', 'open_price', 'tweets', 'sentiment', 'nft_index', 'image']