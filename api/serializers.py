from rest_framework import serializers
from .models import DZIImage


class DZIImageSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    
    class Meta:
        model = DZIImage
        fields = ['id', 'title', 'url', 'created_at']