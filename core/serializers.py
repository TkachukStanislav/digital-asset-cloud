from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Asset
        fields = [
            'id',
            'title',
            'file',
            'thumbnail',
            'file_type',
            'file_size',
            'status',
            'owner',
            'owner_username',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['owner', 'status', 'file_size', 'thumbnail', 'created_at', 'updated_at']