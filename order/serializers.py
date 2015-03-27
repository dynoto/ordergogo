from generic.serializers import DynamicFieldsModelSerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderItem, Item, ItemPhoto

class ItemPhotoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ItemPhoto
        field = ('photo','caption','id')


class ItemSerializer(DynamicFieldsModelSerializer):
    photos = ItemPhotoSerializer(source='itemphoto_set', many=True)

    class Meta:
        model = Item
        field = ('title','description','price','item_photos')

class OrderItemSerializer(DynamicFieldsModelSerializer):
    title          = serializers.ReadOnlyField(source='item.title')
    description    = serializers.ReadOnlyField(source='item.description')
    current_price  = serializers.ReadOnlyField(source='item.price')
    order          = serializers.ReadOnlyField(source='item.price')

    class Meta:
        model = OrderItem
        fields = ('order', 'item', 'title' ,'description' , 'current_price', 'order_price', 'quantity','remarks')

class OrderSerializer(DynamicFieldsModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        field = (Order._meta.get_all_field_names())

class OrderReadSerializer(OrderSerializer):
    location_from = AddressSerializer()
    location_to = AddressSerializer()
    owner = MemberSerializer()
    assigned_to = MemberSerializer()