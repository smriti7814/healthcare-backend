from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctors",
        null=True,      # 👈 ADD THIS
        blank=True     # 👈 ADD THIS
    )
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)