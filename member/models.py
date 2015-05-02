from random import randrange
from generic.models import GenericModel
from django.db import models, IntegrityError
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from os import urandom
# from binascii import hexlify
# from django.utils.timezone import utc
# from django.conf import settings
# import datetime
def generate_photo_name(self, filename):
        url = "media/item/%s/%s%s" % (self.id, randrange(100000,999999), filename)
        return url

# Create your models here.
class Member(AbstractUser):
    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')

    def __str__(self):
        return str(self.username)

    photo       = models.ImageField(upload_to=generate_photo_name, null=True)
    phone       = models.CharField(max_length=64, blank=True)
    mobile      = models.CharField(max_length=64, blank=True)
    fax         = models.CharField(max_length=64, blank=True)
    categories  = models.ManyToManyField('generic.ServiceCategory', through='member.MemberServiceCategory')
    is_vendor   = models.BooleanField(default=False)

    # is_authenticated = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Company(GenericModel):
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return str(self.name)

    name        = models.CharField(max_length=192)
    description = models.TextField(blank=True)
    staffs      = models.ManyToManyField('member.Member', through='member.CompanyStaff')

class CompanyStaff(GenericModel):
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return str(self.name)

    company = models.ForeignKey('member.Company')
    member  = models.ForeignKey('member.Member')

class MemberCategory(GenericModel):
    class Meta:
        unique_together = ('member','category')

    member      = models.ForeignKey('member.Member')
    category    = models.ForeignKey('generic.Category', related_name='member_category')
    verified    = models.BooleanField(default=False)