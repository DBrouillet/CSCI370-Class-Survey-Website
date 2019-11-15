# users/models.py
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    cwid = models.IntegerField(_('cwid'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'cwid'

    # add additional fields in here

    def __str__(self):
        return self.cwid
