from generic.serializers import DynamicFieldsModelSerializer
from member.serializers import MemberSerializer
from credit.models import Package, Transaction

class PackageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Package
        fields = ('id','title','description','price','credits')

class TransactionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id','package','member','amount','transaction_id','is_paypal','is_google','is_apple')
        read_only_fields = ('member','amount','is_paypal','is_apple','is_google')
        extra_kwargs = {
            'package':{'required':True},
            'transaction_id':{'required':True},
        }

class TransactionReadSerializer(TransactionSerializer):
    member = MemberSerializer()
    package = PackageSerializer()