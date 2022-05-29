from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):
    User = models.ForeignKey(User, related_name='requesting_user', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Requests'
        ordering = ('date', "start_time", "end_time")

    def __str__(self):
        return f"{self.User.username.capitalize()}, {self.date}, at {self.start_time}"


class Offer(models.Model):
    User = models.ForeignKey(User, related_name='offering_user', on_delete=models.CASCADE)
    Request = models.ForeignKey(Request, related_name='original_request', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Offerings'
        ordering = ('date', "start_time", "end_time")

    def __str__(self):
        return f"{self.User.username}, {self.date}, at {self.start_time}"

