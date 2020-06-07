from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Product(models.Model):
    product_id = models.IntegerField()
    product_name = models.TextField(default='')
    opinion_amount = models.IntegerField()
    cons_amount = models.IntegerField()
    pros_amount = models.IntegerField()
    mean = models.IntegerField()
    opinions_list = JSONField(default=dict)
    pie = models.ImageField()
    bar = models.ImageField()

    def __str__(self):
        return str(self.product_id)
