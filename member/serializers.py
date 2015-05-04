from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.models import Member, MemberCategory

class MemberCategorySerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer()
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = MemberCategory
        fields = ('category','verified')

class MemberSerializer(DynamicFieldsModelSerializer):
    categories = MemberCategorySerializer(source='membercategory_set', many=True, read_only=True)
    password2  = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Member
        exclude = ('id','password2','last_login','date_joined','is_staff','is_superuser','groups','user_permissions')
        extra_kwargs = {
            'email':{'required':True},
            'username':{'read_only':True},
            'password':{'write_only':True},
        }

class MemberRegisterSerializer(MemberSerializer):

    class Meta:
        model = Member
        fields = ('username','email','password','password2','is_vendor')