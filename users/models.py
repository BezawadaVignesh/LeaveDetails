from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    sid = models.CharField(_('sid'), max_length=10)
    ccl_left = models.IntegerField(_('ccl_left'), null=True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "sid"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=10)
    ccl_left = models.FloatField(default=0)
    ssl_left = models.FloatField(default=0)  # also know as HPl leaves
    epl_left = models.FloatField(default=0)

    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="cls", on_delete=models.CASCADE)
    half = models.BooleanField(default=False)
    on_date = models.DateField()


class CCLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="ccls", on_delete=models.CASCADE)
    half = models.BooleanField(default=False)
    on_date = models.DateField()


class SLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="sls", on_delete=models.CASCADE)
    half = models.BooleanField(default=False)
    on_date = models.DateField()


class EPLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="epls", on_delete=models.CASCADE)
    half = models.BooleanField(default=False)
    on_date = models.DateField()


class Holidays(models.Model):
    on_date = models.DateField()
    desc = models.CharField(max_length=200)
