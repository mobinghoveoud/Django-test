from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime


class Task(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    estimated_time = models.IntegerField()
    details = models.TextField(default="فاقد توضیحات")
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_date_created(self):
        return str(datetime.now().day - self.date_created.day)
