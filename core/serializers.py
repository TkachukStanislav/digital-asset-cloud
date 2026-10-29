from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    # Поле owner_username витягує логін юзера, щоб клієнту було зручно читати
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Asset
        fields = [
            'id',
            'title',
            'file_type',
            'file_size',
            'status',
            'owner',
            'owner_username',
            'created_at',
            'updated_at',
        ]
        # Поле owner буде призначатися бекендом автоматично, тому користувач не повинен вводити його вручну
        read_only_fields = ['owner', 'status', 'created_at', 'updated_at']