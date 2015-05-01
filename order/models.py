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

    PENDING = 'PD'
    ASSIGNED = 'AG'
    COMPLETED = 'CP'
    CANCELLED = 'CC'

    ORDER_STATUS_TYPES = (
        (PENDING,'Pending'),
        (ASSIGNED,'Assigned'),
        (COMPLETED,'Completed'),
        (CANCELLED,'Cancelled'),
    )


    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    remarks     = models.TextField(blank=True)
    category    = models.ForeignKey('generic.Category', blank=True, null=True, on_delete=models.SET_NULL, related_name='order_category')
    status      = models.CharField(max_length=4, choices=ORDER_STATUS_TYPES ,default=PENDING)
    location_from       = models.ForeignKey('location.Address', blank=True, null=True, related_name='order_location_from', on_delete=models.PROTECT)
    location_to         = models.ForeignKey('location.Address', blank=True, null=True, related_name='order_location_to', on_delete=models.PROTECT)
    # tracking_id = models.CharField(max_length=64, blank=True)
    owner       = models.ForeignKey('member.Member', related_name='order_owner', on_delete=models.PROTECT)
    assigned_to = models.ForeignKey('member.Member', blank=True, null=True, on_delete=models.PROTECT, related_name='order_assigned_to')
    objects     = OrderManager()