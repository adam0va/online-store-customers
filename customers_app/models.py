from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import random


class Customer(models.Model):
    name = models.CharField(max_length=200)
    login = models.CharField(default=str(random.randint(10000, 99999)), blank=False, max_length=50)
    orders = ArrayField(models.UUIDField(), null=True, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.name}, login: {self.login}, uuid: {self.uuid}'
