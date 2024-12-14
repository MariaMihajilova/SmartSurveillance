from django.db import models
from datetime import datetime

class Screenshot(models.Model):
    camera_id = models.IntegerField()  # Номер камери
    timestamp = models.DateTimeField(default=datetime.now)  # Дата та час створення
    screenshot = models.ImageField(upload_to='screenshots/')  # Поле для зберігання файлу

    def __str__(self):
        return f"Camera {self.camera_id} - {self.timestamp}"


