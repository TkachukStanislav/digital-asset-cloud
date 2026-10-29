import os
from celery import Celery

# Вказуємо Celery, де шукати налаштування нашого Django-проєкту
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Створюємо екземпляр Celery
app = Celery('digital_asset_cloud')

# Читаємо всі налаштування з settings.py, які починаються з CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично шукаємо задачі (tasks.py) у всіх підключених додатках (зокрема в core)
app.autodiscover_tasks()