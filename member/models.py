from django.db import models,IntegrityError
from django.utils.translation import gettext as _
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

from os import urandom
from binascii import hexlify
from django.utils.timezone import utc
from django.conf import settings
import datetime

# Create your models here.
class Member(AbstractUser):
    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')

    def __str__(self):
        return str(self.id)

    photo = models.URLField(null=True)

    # is_authenticated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(pre_save, sender=Member)
def check_email_duplication(sender, instance, **kwargs):
    if instance.email.strip():
        # Only check duplication if something is given
        members = sender.objects.filter(email=instance.email.strip())

        if instance.id:
            # model being updated
            members = members.exclude(id=instance.id)
            
        if members.exists():
            raise IntegrityError('Email existed')