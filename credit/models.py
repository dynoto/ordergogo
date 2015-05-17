from django.db import models
from generic.models import GenericModel

class Credit(GenericModel):
    member      = models.OneToOneField('member.Member', related_name='member_credits')
    credits     = models.IntegerField(default=0)

class Transaction(GenericModel):
    credit          = models.ForeignKey('credit.Credit')
    transaction_id  = models.CharField(max_length=32, default='') 
# Create your models here.
