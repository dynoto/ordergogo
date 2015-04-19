from random import randrange
from django.db import models
from generic.models import GenericModel
from django.http import Http404
from django.utils.translation import gettext as _

def generate_photo_name(self, filename):
        url = "media/item/%s/%s%s" % (self.item.id, randrange(100000,9999999), filename[-5:])
        return url
# Create your models here.

class OrderManager(models.Manager):
    def get_assigned_order(self, user, order_id):
        try:
            return Order.objects.get(assigned_to=user, id=order_id)
        except:
            raise Http404

class Order(GenericModel):
    def __str__(self):
        return "%s" %(self.title)


    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    remarks     = models.TextField(blank=True)
    # is_assigned = models.BooleanField(default=False)
    # is_delivered= models.BooleanField(default=False)
    service     = models.ForeignKey('order.ServiceType', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_service_type')
    status      = models.ForeignKey('order.OrderStatus', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_status')
    assigned_to = models.ForeignKey('member.Member', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_assigned_to')
    location_from       = models.ForeignKey('location.Address', related_name='order_location_from', on_delete=models.PROTECT)
    location_to         = models.ForeignKey('location.Address', related_name='order_location_to', on_delete=models.PROTECT)
    # reference_number    = models.CharField(max_length=64, unique=True, blank=True, default=)
    tracking_id = models.CharField(max_length=64, blank=True)
    owner       = models.ForeignKey('member.Member', related_name='order_owner', on_delete=models.PROTECT)
    items       = models.ManyToManyField('order.Item', through='order.OrderItem')
    objects     = OrderManager()

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
    photo       = models.ImageField(upload_to=generate_photo_name)
    owner       = models.ForeignKey('member.Member', related_name='item_photo_owner', on_delete=models.PROTECT)


class OrderItem(GenericModel):
    quantity    = models.IntegerField()
    remarks     = models.TextField(blank=True)
    order_price = models.FloatField(null=True, blank=True) #sometimes price can change after order has been made, this is to ensure it keeps the record when order been made
    order       = models.ForeignKey('order.Order')
    item        = models.ForeignKey('order.Item')


class OrderStatus(GenericModel):
    class Meta:
        verbose_name_plural = _('Order Statuses')

    def __str__(self):
        return "%s" %(self.title)
    title       = models.CharField(max_length=64)
    owner       = models.ForeignKey('member.Member', related_name='order_status_owner', on_delete=models.PROTECT)


class ServiceType(GenericModel):
    def __str__(self):
        return "%s" %(self.title)
    title       = models.CharField(max_length=64)
    owner       = models.ForeignKey('member.Member', related_name='order_type_owner', on_delete=models.PROTECT)

class OrderReject(GenericModel):
    class Meta:
        verbose_name_plural = _('Order Rejections')