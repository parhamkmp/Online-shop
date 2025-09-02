import os
from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICE = (

    ('admin','Admin'),
    ('buyer','Buyer'),
    ('superuser','SuperUser'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICE, default='buyer')
    phone_number = models.CharField(blank=False, null=False, max_length=11, unique=True)
    address = models.TextField(null=False, blank=False, max_length=2000)
    image_profile = models.ImageField(upload_to='profile_img', blank=True, null=True)


    def delete(self, *args, **kwargs):
        if self.image_profile and os.path.isfile(self.image_profile.path):
            os.remove(self.image_profile.path)
        super().delete(*args, **kwargs)
