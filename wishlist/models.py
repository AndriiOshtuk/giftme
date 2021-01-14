from django.db import models


from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50, blank=True)
    phone_number = PhoneNumberField(help_text='Phone number')

    # TODO Add __str__()


class WishList(models.Model):
    name = models.CharField(max_length = 50)
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey('Gift', on_delete=models.CASCADE)

    # TODO Add __str__()


class Gift(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(help_text='Gift description, details, etc.')
    price = models.PositiveIntegerField()
    url = models.URLField()
    photo = models.ImageField(upload_to='gifts_images')
    wish_list = models.ForeignKey('WishList', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_DEFAULT, default=None)

    # TODO Add __str__()      
