from django.db import models
from django.contrib.postgres.fields import ArrayField
import random


class Customer(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(default=str(random.randint(10000, 99999)), blank=False, max_length=50)
    orders = ArrayField(models.UUIDField(), null=True, blank=True)
    user_id = models.PositiveIntegerField(null=False, blank=False, unique=True, primary_key = True)

    def __str__(self):
        return f'{self.name}, login: {self.username}, user_id: {self.user_id}'
