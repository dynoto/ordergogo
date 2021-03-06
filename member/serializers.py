from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
# from location.serializers import CountrySerializer
from member.models import Member, MemberCategory, MemberVerification, MemberReferral

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
    username    = serializers.EmailField(validators=[UniqueValidator(queryset=Member.objects.all())])
    country_code= serializers.IntegerField()
    categories  = MemberCategorySerializer(source='membercategory_set', many=True, read_only=True)
    password2   = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Member
        fields = ('username','first_name','last_name','password','password2','is_vendor','is_active','country_code','phone','categories','created_at','updated_at')
        extra_kwargs = {
            # 'email':{'required':True},
            'password':{'write_only':True},
            'username':{'read_only':True},
            'is_vendor':{'read_only':True}
        }

class MemberRegisterSerializer(MemberSerializer):

    class Meta:
        model = Member
        fields = ('username','password','password2','phone','country_code','is_vendor','referral')
        extra_kwargs = {
            # 'email':{'required':True},
            'username':{'required':True},
            'is_vendor':{'required':True},
            'phone':{'required':True},
            'country_code':{'required':True}
        }

class MemberPhotoSerializer(MemberSerializer):
    class Meta:
        model = Member
        fields = ('photo',)

class MemberVerificationSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MemberVerification
        fields = ('member','code','verified')
        read_only_fields = ('member','verified')

class MemberReferralSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = MemberReferral
        fields = ('member','code','referred')
        read_only_fields = ('member','referred')