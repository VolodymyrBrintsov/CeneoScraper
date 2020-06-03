# Generated by Django 3.0.4 on 2020-06-03 20:56

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20200603_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bar',
            field=models.ImageField(default='', upload_to='opinions_analyze'),
        ),
        migrations.AddField(
            model_name='product',
            name='pie',
            field=models.ImageField(default='', upload_to='opinion_analyze'),
        ),
        migrations.AlterField(
            model_name='product',
            name='opinions_list',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]