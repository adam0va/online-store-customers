from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Customer(models.Model):
    name = models.CharField(max_length=200)
    login = models.CharField(default = '0', blank=False, max_length=50)
    orders = ArrayField(models.UUIDField(), null=True, blank=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.name}, uuid: {self.uuid}'
