# Generated by Django 3.1.5 on 2021-01-15 09:30

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0003_auto_20210114_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, help_text='Phone number', max_length=128, region=None, unique=True),
        ),
    ]
