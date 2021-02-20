# Generated by Django 3.1.5 on 2021-01-23 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wishlist", "0007_auto_20210116_1504"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gift",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="wishlist.user",
            ),
        ),
    ]
