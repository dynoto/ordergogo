from django.contrib.gis.db import models


# Create your models here.
class Address(models.Model):
    gps_location    = models.PointField(null=True)

    address_name    = models.CharField(max_length=255, blank=True,default="")
    address_line_1  = models.CharField(max_length=255, blank=True,default="")
    address_line_2  = models.CharField(max_length=255, blank=True,default="")
    postal_code     = models.CharField(max_length=255, blank=True,default="")
    state           = models.CharField(max_length=255, blank=True,default="")

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects = models.GeoManager()