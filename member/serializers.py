from rest_framework import serializers
from member.models import Member

class MemberSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (Member._meta_get_all_field_names())