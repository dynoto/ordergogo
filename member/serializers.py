from rest_framework import serializers
from generic.serializers import DynamicFieldsModelSerializer
from member.models import Member

class MemberSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Member
        exclude = ('password','is_superuser','is_staff','is_active','groups','user_permissions')
        field = ('id','first_name','last_name','username','email','photo')