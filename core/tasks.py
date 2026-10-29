import time
from celery import shared_task
from .models import Asset
from .mongo import metadata_collection


@shared_task
def process_asset_task(asset_id):
    """
    Фонова задача Celery для обробки файлу.
    Працює асинхронно поза межами HTTP-запиту.
    """
    try:
        # 1. Знаходимо файл у базі
        asset = Asset.objects.get(id=asset_id)
        
        # 2. Оновлюємо статус на 'processing'
        asset.status = 'processing'
        asset.save(update_fields=['status'])

        # 3. Імітуємо важку роботу (наприклад, оптимізація, підрахунок хешу)
        time.sleep(5)

        # 4. Дописуємо лог успіху та технічні параметри в MongoDB
        metadata_collection.update_one(
            {"asset_id": asset_id},
            {
                "$push": {"processing_logs": "File processed successfully by Celery worker"},
                "$set": {"processed_by": "celery_v1", "compression_ratio": "0.75"}
            },
            upsert=True
        )

        # 5. Оновлюємо фінальний статус у SQLite
        asset.status = 'completed'
        asset.save(update_fields=['status'])
        
        return f"Asset {asset_id} processed successfully"

    except Asset.DoesNotExist:
        return f"Asset {asset_id} not found"