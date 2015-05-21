import requests, string
from ordergogo.settings import HOOIO_SENDER, HOOIO_ACCESS_TOKEN, HOOIO_APP_ID
from random import randrange, SystemRandom
from generic.models import GenericModel
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser

def generate_photo_name(self, filename):
    url = "media/item/%s/%s%s" % (self.id, randrange(100000,999999), filename)
    return url

def generate_referral():
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(7))

# Create your models here.
class Member(AbstractUser):
    class Meta:
        
        verbose_name_plural = _('Members')

    def __str__(self):
        return str(self.username)

    def __unicode__(self):
        return str(self.username)

    photo       = models.ImageField(upload_to=generate_photo_name, null=True, blank=True)
    phone       = models.CharField(max_length=64, unique=True)
    country_code= models.CharField(max_length=4, blank=True, default="65")
    categories  = models.ManyToManyField('generic.Category', through='member.MemberCategory')
    country     = models.ForeignKey('location.Country', blank=True, null=True)
    is_vendor   = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    credit      = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    referral    = models.ForeignKey('member.MemberReferral', blank=True, null=True, related_name='referred_by_member')


    # is_authenticated = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class Company(GenericModel):
    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
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

    def __unicode__(self):
        return str(self.name)

    company = models.ForeignKey('member.Company')
    member  = models.ForeignKey('member.Member')

class MemberCategoryManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(MemberCategoryManager, self).get_queryset().filter(verified=True)


class MemberCategory(GenericModel):
    class Meta:
        unique_together = ('member','category')

    def __unicode__(self):
        return str('Member Category')

    member      = models.ForeignKey('member.Member')
    category    = models.ForeignKey('generic.Category', related_name='member_category')
    verified    = models.BooleanField(default=False)

    objects = MemberCategoryManager()


class MemberVerification(GenericModel):
    member      = models.OneToOneField('member.Member')
    code        = models.CharField(max_length=16, default=randrange(100000,999999))
    verified    = models.BooleanField(default=False)

    def send_code(self, country_code, phone, verification_code):
        message = "Your verification number is %s" % (verification_code)
        hooio_url = "https://secure.hoiio.com/open/sms/send?dest=+%s%s&sender_name=%s&msg=%s&access_token=%s&app_id=%s" % (country_code, phone, HOOIO_SENDER, message, HOOIO_ACCESS_TOKEN, HOOIO_APP_ID)
        return requests.get(hooio_url)

class MemberReferral(GenericModel):
    member      = models.OneToOneField('member.Member')
    code        = models.CharField(max_length=8, default=generate_referral, primary_key=True)
    referred    = models.IntegerField(default=0)