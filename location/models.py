from django.utils.translation import gettext as _
from django.contrib.gis.db import models


# Create your models here.
class Address(models.Model):
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


    def __str__(self):
        return "%s %s" %(self.address_line_1, self.address_line_2)

    gps_location    = models.PointField(null=True, blank=True)

    address_name    = models.CharField(max_length=255, blank=True,default="")
    address_line_1  = models.CharField(max_length=255, blank=True,default="")
    address_line_2  = models.CharField(max_length=255, blank=True,default="")
    postal_code     = models.CharField(max_length=255, blank=True,default="")

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    owner           = models.ForeignKey('member.Member', related_name='address_owner')
    area            = models.ForeignKey('location.Area', related_name='address_area', on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.GeoManager()

class Area(models.Model):
    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    area_name       = models.CharField(max_length=255, blank=True,default="")
    gps_location    = models.PointField(null=True, blank=True)
    objects         = models.GeoManager()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    owner           = models.ForeignKey('member.Member', related_name='area_owner', null=True, blank=True)
