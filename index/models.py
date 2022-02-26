from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Work(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    estimated_time = models.IntegerField()
    detail = models.TextField(default="فاقد توضیحات")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
