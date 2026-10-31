from django.db import models
from django.contrib.auth.models import User


class Asset(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    thumbnail = models.FileField(upload_to='thumbnails/%Y/%m/%d/', blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title