from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    email = models.EmailField('Email Address', unique=True)
    first_name = models.CharField("First Name", max_length=150, blank=True)
    last_name = models.CharField("Last Name", max_length=150, blank=True)
    username = models.CharField("Username", max_length=150)
    full_name = models.CharField("Full Name", max_length=150)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.username = self.first_name.lower() + '.' + self.last_name.lower()
        self.full_name = self.first_name + "  " + self.last_name
        super().save(*args, **kwargs)