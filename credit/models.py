from django.db import models
from generic.models import GenericModel

class Credit(GenericModel):
    member      = models.OneToOneField('member.Member', related_name='member_credits')
    credits     = models.IntegerField(default=0)


class Package(GenericModel):
    title       = models.CharField(max_length=254)
    description = models.TextField(default='', blank=True)
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    credits     = models.IntegerField()


class Transaction(GenericModel):
    package         = models.ForeignKey('credit.Package')
    credit          = models.ForeignKey('credit.Credit')
    transaction_id  = models.CharField(max_length=32, default='') 
