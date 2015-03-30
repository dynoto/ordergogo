from random import randrange
from django.db import models
from generic.models import GenericModel

def generate_photo_name(self, filename):
        url = "media/item/%s/%s%s" % (self.item.id, randrange(100000,999999), filename)
        return url
# Create your models here.
class Order(GenericModel):
    def __str__(self):
        return "%s" %(self.title)


    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    remarks     = models.TextField(blank=True)
    is_assigned = models.BooleanField(default=False)
    is_delivered= models.BooleanField(default=False)
    assigned_to = models.ForeignKey('member.Member', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_assigned_to')
    location_from       = models.ForeignKey('location.Address', related_name='order_location_from', on_delete=models.PROTECT)
    location_to         = models.ForeignKey('location.Address', related_name='order_location_to', on_delete=models.PROTECT)
    # reference_number    = models.CharField(max_length=64, unique=True, blank=True, default=)
    tracking_id = models.CharField(max_length=64, blank=True)
    owner       = models.ForeignKey('member.Member', related_name='order_owner', on_delete=models.PROTECT)
    items       = models.ManyToManyField('order.Item', through='order.OrderItem')



class Item(GenericModel):
    def __str__(self):
        return "%s" %(self.title)

    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    price       = models.FloatField(null=True)
    owner       = models.ForeignKey('member.Member', related_name='item_owner', on_delete=models.PROTECT)

class ItemPhoto(GenericModel):

    item        = models.ForeignKey('order.Item')
    caption     = models.CharField(max_length=254, default='', blank=True)
    photo       = models.ImageField(upload_to=generate_photo_name, null=True)
    owner       = models.ForeignKey('member.Member', related_name='item_photo_owner', on_delete=models.PROTECT)

class OrderItem(GenericModel):
    quantity    = models.IntegerField()
    remarks     = models.TextField(blank=True)
    order_price = models.FloatField(null=True, blank=True) #sometimes price can change after order has been made, this is to ensure it keeps the record when order been made
    order       = models.ForeignKey('order.Order')
    item        = models.ForeignKey('order.Item')