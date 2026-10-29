from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    # Статуси обробки файлу для нашого майбутнього Celery
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    # Власник файлу (Foreign Key на стандартного User Django).
    # on_delete=models.CASCADE означає: видалили юзера — видалилися і його файли.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    
    # Назва та мета-параметри
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField(help_text="Розмір файлу в байтах")
    
    # Поточний статус обробки фоновими задачами
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Часові мітки (аналог created_at / updated_at у FastAPI)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"