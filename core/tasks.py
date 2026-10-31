import io
import os
from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile
from .models import Asset
from .mongo import get_asset_metadata_collection


@shared_task
def process_asset_task(asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
        asset.status = 'processing'
        asset.save(update_fields=['status'])

        meta_collection = get_asset_metadata_collection()

        # Перевіряємо, чи є завантажений файл зображенням
        file_ext = os.path.splitext(asset.file.name)[1].lower()
        is_image = file_ext in ['.jpg', '.jpeg', '.png', '.webp']

        metadata_update = {
            'processed_by': 'celery_worker',
            'is_image': is_image,
        }

        if is_image and asset.file:
            # Читаємо оригінальний файл напряму зі сховища S3
            image = Image.open(asset.file)
            orig_width, orig_height = image.size

            metadata_update['original_dimensions'] = {
                'width': orig_width,
                'height': orig_height,
            }

            # Створюємо мініатюру (максимальний розмір 250x250)
            image.thumbnail((250, 250))

            # Зберігаємо результат в оперативну пам'ять
            thumb_io = io.BytesIO()
            img_format = 'PNG' if file_ext == '.png' else 'JPEG'
            image.save(thumb_io, format=img_format, quality=85)

            # Формуємо ім'я та зберігаємо мініатюру в поле thumbnail
            thumb_name = f"thumb_{os.path.basename(asset.file.name)}"
            asset.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)

        asset.status = 'completed'
        asset.save()

        # Оновлюємо метадані та історію обробки в MongoDB
        meta_collection.update_one(
            {'asset_id': asset.id},
            {
                '$set': metadata_update,
                '$push': {'processing_logs': 'Thumbnail generated and asset processed successfully'}
            }
        )

        return f"Asset {asset_id} processed successfully"

    except Asset.DoesNotExist:
        return f"Asset {asset_id} not found"
    except Exception as e:
        if 'asset' in locals():
            asset.status = 'failed'
            asset.save(update_fields=['status'])
        raise e