from django.contrib.auth.models import User
from django.db import models


class Verify(models.Model):
    verify_code = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.verify_code
