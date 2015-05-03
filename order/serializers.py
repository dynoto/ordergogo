from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderLocation, OrderBid

class OrderLocationSerializer(AddressSerializer):
    class Meta:
        model = OrderLocation
        fields = (OrderLocation._meta.get_all_field_names())

class OrderSerializer(DynamicFieldsModelSerializer):
    category    = CategorySerializer()
    location_from = OrderLocationSerializer
    location_to = OrderLocationSerializer
    tracking_id = serializers.CharField(read_only=True)
    status      = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = (Order._meta.get_all_field_names())
        exclude = ('description')

class OrderCategorySerializer(OrderSerializer):
    class Meta:
        fields = ('category',)

class OrderAssignSerializer(OrderSerializer):
    class Meta:
        fields = ('assigned_to',)

class OrderReadSerializer(OrderSerializer):
    location_from = AddressSerializer()
    location_to = AddressSerializer()
    owner = MemberSerializer()
    assigned_to = MemberSerializer()

class OrderBidSerializer(DynamicFieldsModelSerializer):
    # order = OrderSerializer()

    class Meta:
        model = OrderBid
        fields = ('order','owner','remarks','accepted')