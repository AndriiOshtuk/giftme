from django.db import models


from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50, blank=True)
    phone_number = PhoneNumberField(help_text='Phone number')      
