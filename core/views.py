from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Asset
from .serializers import AssetSerializer
from .mongo import metadata_collection
from .tasks import process_asset_task

class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Asset.objects.all().order_by('-created_at')
        return Asset.objects.filter(owner=user).order_by('-created_at')

    def perform_create(self, serializer):
            asset = serializer.save(owner=self.request.user)
            # Створюємо базовий початковий документ у MongoDB
            metadata_collection.insert_one({
                "asset_id": asset.id,
                "tags": [],
                "custom_attributes": {},
                "processing_logs": ["Asset record created in SQLite"]
            })
            
            # Відправляємо задачу у чергу Celery!
            # .delay() не блокує виконання коду, а миттєво віддає id задачі в RabbitMQ
            process_asset_task.delay(asset.id)

    def retrieve(self, request, *args, **kwargs):
        # Перевизначаємо отримання одного запису (GET /api/assets/{id}/)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Шукаємо документ у MongoDB за asset_id
        mongo_data = metadata_collection.find_one({"asset_id": instance.id})
        if mongo_data:
            # MongoDB за замовчуванням додає свій внутрішній ключ '_id' типу ObjectId,
            # який не серіалізується в звичайний JSON, тому видаляємо його або робимо рядком
            mongo_data.pop('_id', None)
            data['metadata'] = mongo_data
        else:
            data['metadata'] = None

        return Response(data)

    @action(detail=True, methods=['post'], url_path='metadata')
    def add_metadata(self, request, pk=None):
        """
        Кастомний ендпоінт: POST /api/assets/{id}/metadata/
        Дозволяє додавати будь-які довільні поля без фіксованої схеми.
        """
        asset = self.get_object()
        payload = request.data  # отримуємо будь-який JSON від клієнта

        # Оновлюємо документ у MongoDB ($set додає або оновлює зазначені поля)
        metadata_collection.update_one(
            {"asset_id": asset.id},
            {"$set": {"custom_attributes": payload}},
            upsert=True
        )

        return Response(
            {"status": "success", "message": "Metadata updated in MongoDB", "data": payload},
            status=status.HTTP_200_OK
        )