from django.contrib.auth.models import User
from django.db import models


class Verify(models.Model):
    verify_code = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.verify_code

class Role(models.Model):
    role = models.IntegerField() # 1 => Broker & 2 => Contractor
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.role

    def get_role(self):
        if self.role == 1:
            return "کارگزار"
        else:
            return "پیمانکار"