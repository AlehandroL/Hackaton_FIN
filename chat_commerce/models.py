from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    User = models.ForeignKey(User, related_name='requesting_user', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Requests'
        ordering = ('date', "time")

    def __str__(self):
        return self.User.username


class Offer(models.Model):
    User = models.ForeignKey(User, related_name='offering_user', on_delete=models.CASCADE)
    Request = models.ForeignKey(Request, related_name='original_request', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Offerings'
        ordering = ('date', "time")

    def __str__(self):
        return self.User.username

