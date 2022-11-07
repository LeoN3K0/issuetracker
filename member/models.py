from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return self.user.full_name

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 150 or img.width > 150:
            new_img = (150, 150)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class AccessRequest(models.Model):
    first_name = models.CharField("First Name", max_length=150, blank=True)
    last_name = models.CharField("Last Name", max_length=150, blank=True)
    email = models.EmailField('Email Address', unique=True)
    reason = models.TextField('Reason')
    request_date = models.DateTimeField('Request Date', blank=True, null=True,)

    def __str__(self):
        return self.first_name