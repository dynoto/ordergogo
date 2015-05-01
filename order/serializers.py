from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
# from rest_framework import serializers
from order.models import Order

class OrderSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Order
        field = (Order._meta.get_all_field_names())
        exclude = ('description','created_at','updated_at')

class OrderReadSerializer(OrderSerializer):
    location_from = AddressSerializer()
    location_to = AddressSerializer()
    owner = MemberSerializer()
    assigned_to = MemberSerializer()