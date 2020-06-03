from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Product(models.Model):
    product_id = models.IntegerField()
    opinion_amount = models.IntegerField()
    cons_amount = models.IntegerField()
    pros_amount = models.IntegerField()
    mean = models.IntegerField()
    opinions_list = JSONField(default='')

    def __str__(self):
        return str(self.product_id)