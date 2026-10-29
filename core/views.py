from rest_framework import viewsets
from .models import Asset
from .serializers import AssetSerializer

class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        # Користувач бачить лише власні завантажені файли
        # Якщо це суперюзер/адмін — показуємо взагалі всі файли в системі
        user = self.request.user
        if user.is_staff:
            return Asset.objects.all().order_by('-created_at')
        return Asset.objects.filter(owner=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Коли створюється новий запис через POST, автоматично записуємо поточного юзера як власника
        serializer.save(owner=self.request.user)