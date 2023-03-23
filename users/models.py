from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    # username = None
    '''
    Base class definition for username
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    '''
    email = models.EmailField(_('email address'), unique=True)
    sid = models.IntegerField(_('sid'))
    ccl_left = models.IntegerField(_('ccl_left'))
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "sid"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class CLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="cls", on_delete=models.CASCADE)
    on_date = models.DateField()


class CCLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="ccls", on_delete=models.CASCADE)
    on_date = models.DateField()


class SLS(models.Model):
    user = models.ForeignKey(CustomUser, related_name="sls", on_delete=models.CASCADE)
    on_date = models.DateField()
