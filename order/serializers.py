from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderAddress, OrderBid

class OrderAddressSerializer(AddressSerializer):
    class Meta:
        model = OrderAddress
        fields = (OrderAddress._meta.get_all_field_names())

class OrderSerializer(DynamicFieldsModelSerializer):
    category    = CategorySerializer()
    location_from = OrderAddressSerializer()
    location_to = OrderAddressSerializer()
    tracking_id = serializers.CharField(read_only=True)
    status      = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('title','description','category','status','preferred_time','location_from','location_to','tracking_id','assigned_to','owner')

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