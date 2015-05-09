from generic.serializers import DynamicFieldsModelSerializer, CategorySerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderAddress, OrderBid

class OrderAddressSerializer(AddressSerializer):
    class Meta:
        model = OrderAddress
        fields = ('address_name','gps_location','address_line_1','address_line_2','postal_code','area')

class OrderSerializer(DynamicFieldsModelSerializer):
    location_from = OrderAddressSerializer()

    class Meta:
        model = Order
        fields = ('id','title','description','category','status','preferred_time','location_from','tracking_id','owner','assigned_to')
        read_only_fields = ('tracking_id','status','owner','assigned_to')

    def create(self, validated_data):
        order_address = validated_data.pop('location_from')
        order_address['owner'] = validated_data['owner']
        order_address = OrderAddress.objects.create(**order_address)

        validated_data['location_from'] = order_address
        return Order.objects.create(**validated_data)
        # order.location_from = order_address
        # order.save()


class OrderAssignSerializer(OrderSerializer):
    class Meta:
        fields = ('assigned_to',)

class OrderReadSerializer(OrderSerializer):
    owner = MemberSerializer(exclude=('categories',))
    category = CategorySerializer()
    assigned_to = MemberSerializer(exclude=('categories',))

class OrderBidSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = OrderBid
        fields = ('order','owner','price','remarks','accepted')
        read_only_fields = ('accepted',)