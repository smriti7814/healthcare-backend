from django.db import models
from django.conf import settings


class Patient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   
        on_delete=models.CASCADE,
        related_name="patients"
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    address = models.TextField(default="Unknown")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name