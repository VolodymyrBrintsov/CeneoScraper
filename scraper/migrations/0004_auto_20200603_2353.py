# Generated by Django 3.0.4 on 2020-06-03 20:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_delete_productopinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='opinions_list',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]