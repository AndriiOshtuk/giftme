# Generated by Django 3.1.5 on 2021-01-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0006_auto_20210115_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='description',
            field=models.TextField(blank=True, help_text='Gift description, details, etc.'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='gifts_images'),
        ),
        migrations.AlterField(
            model_name='gift',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gift',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]