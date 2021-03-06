# Generated by Django 3.0.4 on 2020-06-03 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('opinion_amount', models.IntegerField()),
                ('cons_amount', models.IntegerField()),
                ('pros_amount', models.IntegerField()),
                ('mean', models.IntegerField()),
                ('opinions_file', models.FileField(default='', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOpinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion_id', models.IntegerField()),
                ('author', models.CharField(max_length=255)),
                ('recommendation', models.CharField(max_length=30)),
                ('stars', models.CharField(max_length=5)),
                ('usefull', models.IntegerField()),
                ('useless', models.IntegerField()),
                ('content', models.CharField(max_length=2000)),
                ('cons', models.CharField(blank=True, max_length=355, null=True)),
                ('pros', models.CharField(blank=True, max_length=355, null=True)),
                ('purchased', models.BooleanField()),
                ('review_date', models.CharField(blank=True, max_length=355, null=True)),
                ('purchase_date', models.CharField(blank=True, max_length=355, null=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Product')),
            ],
        ),
    ]
