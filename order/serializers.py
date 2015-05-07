from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderBid

class OrderSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Order
        fields = ('title','description','category','status','preferred_time','location_from','tracking_id','assigned_to','owner')
        extra_kwargs = {
            'status' : {'read_only':True},
            'tracking_id' : {'read_only':True},
            'deleted' : {'read_only':True}
        }

class OrderReadSerializer(OrderSerializer):
    category    = CategorySerializer(read_only=True)
    location_from = AddressSerializer(read_only=True)

class OrderCategorySerializer(OrderSerializer):
    class Meta:
        fields = ('category',)

class OrderAssignSerializer(OrderSerializer):
    class Meta:
        fields = ('assigned_to',)

class OrderReadSerializer(OrderSerializer):
    owner = MemberSerializer()
    assigned_to = MemberSerializer()

class OrderBidSerializer(DynamicFieldsModelSerializer):
    # order = OrderSerializer()

    class Meta:
        model = OrderBid
        fields = ('order','owner','remarks','accepted')