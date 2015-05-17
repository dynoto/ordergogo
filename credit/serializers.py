from generic.serializers import DynamicFieldsModelSerializer
from member.serializers import MemberSerializer
from credit.models import Credit, Package, Transaction

class PackageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Package
        fields = ('id','title','description','price','credits')