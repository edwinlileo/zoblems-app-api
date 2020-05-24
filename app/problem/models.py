from django.db import models
from django.conf import settings


class Response(models.Model):
    """Response to be used in a problem"""
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.description
