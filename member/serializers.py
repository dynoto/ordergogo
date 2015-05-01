# from rest_framework import serializers
from generic.serializers import DynamicFieldsModelSerializer
from member.models import Member, MemberCategory

class MemberSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Member
        exclude = ('password','is_superuser','is_staff','is_active','groups','user_permissions','last_login','date_joined','created_at','updated_at')
        field = ('id','first_name','last_name','username','email','photo','phone','mobile','fax')

class MemberCategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MemberCategory
        field = ('member','category','verified')