from django.db import models
from generic.models import Photo

# Create your models here.
class Order(models.Model):
    title       = models.CharField(max_length=64)
    description = models.TextField(null=True)
    remarks     = models.TextField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)
    is_delivered= models.BooleanField(default=False)
    created_by  = models.ForeignKey('member.Member', related_name='order_created_by')
    assigned_to = models.ForeignKey('member.Member', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_assigned_to')
    location_from       = models.ForeignKey('location.Address', related_name='order_location_from')
    location_to         = models.ForeignKey('location.Address', related_name='order_location_to')
    reference_number    = models.CharField(max_length=64, unique=True)

class Item(models.Model):
    title       = models.CharField(max_length=64)
    description = models.TextField(null=True)
    price       = models.FloatField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    created_by  = models.ForeignKey('member.Member', related_name='item_created_by')

class ItemPhoto(Photo):
    item        = models.ForeignKey('order.Item')

class OrderItem(models.Model):
    quantity    = models.IntegerField()
    remarks     = models.TextField(null=True)
    price       = models.FloatField(null=True) #sometimes price can change after order has been made, this is to ensure it keeps the record when order been made
    order       = models.ForeignKey('order.Order')
    item        = models.ForeignKey('order.Item')