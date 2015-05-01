from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderLocation

class OrderLocationSerializer(AddressSerializer):
    class Meta:
        model = OrderLocation
        field = (OrderLocation._meta.get_all_field_names())

class OrderSerializer(DynamicFieldsModelSerializer):
    category    = CategorySerializer()
    location_from = OrderLocationSerializer
    location_to = OrderLocationSerializer
    tracking_id = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        field = (Order._meta.get_all_field_names())
        exclude = ('description',)

class OrderReadSerializer(OrderSerializer):
    location_from = AddressSerializer()
    location_to = AddressSerializer()
    owner = MemberSerializer()
    assigned_to = MemberSerializer()