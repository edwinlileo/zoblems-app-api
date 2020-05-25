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


class Problem(models.Model):
    """Problem"""
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    accessUsers = models.ManyToManyField('user.User', blank=True, \
                                          related_name='problems')
    responses = models.ManyToManyField('problem.Response', related_name='problem')

    def __str__(self):
        return self.title
