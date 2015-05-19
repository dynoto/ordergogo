from django.db import models
from generic.models import GenericModel

class Package(GenericModel):
    title       = models.CharField(max_length=254)
    description = models.TextField(default='', blank=True)
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    credits     = models.IntegerField()


class Transaction(GenericModel):
    package         = models.ForeignKey('credit.Package')
    member          = models.ForeignKey('member.Member')
    amount          = models.DecimalField(max_digits=6, decimal_places=2)
    transaction_id  = models.CharField(max_length=32, default='', blank=True)
    is_paypal       = models.BooleanField(default=False)
    is_google       = models.BooleanField(default=False)
    is_apple        = models.BooleanField(default=False)
