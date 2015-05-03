import random,string
from random import randrange
from django.db import models
from generic.models import GenericModel
from django.http import Http404
# from django.utils.translation import gettext as _
from location.models import Address

def generate_photo_name(self, filename):
        url = "media/item/%s/%s%s" % (self.item.id, randrange(100000,9999999), filename[-5:])
        return url

def generate_long_order_id():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

# Create your models here.

class OrderManager(models.Manager):
    def get_assigned_order(self, order_id, user):
        try:
            return Order.objects.get(assigned_to=user, id=order_id)
        except:
            raise Http404

    def get_order_from_owner(self, order_id, user):
        try:
            return Order.objects.get(owner=user, id=order_id)
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
    category    = models.ForeignKey('generic.Category', related_name='order_category')
    status      = models.CharField(max_length=4, choices=ORDER_STATUS_TYPES ,default=PENDING)
    preferred_time      = models.DateTimeField(null=True, blank=True)
    location_from       = models.ForeignKey('order.OrderLocation', blank=True, null=True, related_name='order_location_from')
    location_to         = models.ForeignKey('order.OrderLocation', blank=True, null=True, related_name='order_location_to')
    tracking_id = models.CharField(max_length=64, default=generate_long_order_id())
    owner       = models.ForeignKey('member.Member', related_name='order_owner', on_delete=models.PROTECT)
    assigned_to = models.ForeignKey('member.Member', blank=True, null=True, on_delete=models.PROTECT, related_name='order_assigned_to')
    objects     = OrderManager()

# this model is created
class OrderLocation(Address):
    order       = models.ForeignKey('order.Order', related_name='order_location')

class OrderBid(GenericModel):
    class Meta:
        unique_together = ('order','owner')

    order       = models.ForeignKey('order.Order', related_name='order_bid_order')
    owner       = models.ForeignKey('member.Member', related_name='order_bid_owner')
    remarks     = models.CharField(blank=True, max_length=254)
    accepted    = models.BooleanField(default=False)