from rest_framework import serializers
from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.models import Member, MemberCategory

class MemberCategorySerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer()
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = MemberCategory
        fields = ('category','verified')
        extra_kwargs = {
            'member':{'required':False,'read_only':True}
        }

class MemberSerializer(DynamicFieldsModelSerializer):
    categories = MemberCategorySerializer(source='membercategory_set', many=True, read_only=True)
    password2  = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Member
        fields = ('email','username','first_name','last_name','password','password2','is_vendor','is_active','phone','mobile','fax','categories','created_at','updated_at')
        extra_kwargs = {
            'email':{'required':True},
            'username':{'read_only':True},
            'password':{'write_only':True},
            'is_vendor':{'read_only':True},
        }

class MemberRegisterSerializer(MemberSerializer):

    class Meta:
        model = Member
        fields = ('username','email','password','password2','is_vendor')
        extra_kwargs = {
            'email':{'required':True},
            'username':{'required':True},
            'password':{'required':True},
            'is_vendor':{'required':True},
        }