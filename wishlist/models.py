import datetime

from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class WishList(models.Model):
    name = models.CharField(max_length=50)
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Wishlist:{self.name}"

    def is_due(self):
        return self.due_date < datetime.date.today()


class Gift(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(
        blank=True, help_text="Gift description, details, etc."
    )
    price = models.PositiveIntegerField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to="gifts_images")
    wish_list = models.ForeignKey("WishList", on_delete=models.CASCADE, null=True)
    is_booked = models.BooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True
    )

    def __str__(self):
        return f"Gift:{self.name} in {self.wish_list}"
