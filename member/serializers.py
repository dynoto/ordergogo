from rest_framework import serializers
from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.models import Member, MemberCategory

class MemberCategorySerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer()
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = MemberCategory
        field = ('member','category','verified')

class MemberSerializer(DynamicFieldsModelSerializer):
    categories = MemberCategorySerializer(source='category_set', many=True, read_only=True)

    class Meta:
        model = Member
        exclude = ('id','is_superuser','is_staff','is_active','groups','user_permissions','last_login','date_joined','created_at','updated_at')
        field = ('first_name','last_name','username','email','photo','phone','mobile','fax','password')