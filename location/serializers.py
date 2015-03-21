from generic.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from location.models import Address

class AddressSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Address
        field = (Address._meta.get_all_field_names())

