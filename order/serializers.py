from generic.serializers import DynamicFieldsModelSerializer
from member.serializers import MemberSerializer
from location.serializers import AddressSerializer
from rest_framework import serializers
from order.models import Order, OrderItem, Item, ItemPhoto, ServiceType, OrderStatus

class ServiceTypeSerializer(DynamicFieldsModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ServiceType
        field = ('id','title')


class OrderStatusSerializer(DynamicFieldsModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = OrderStatus
        field = ('id','title')



class ItemPhotoSerializer(DynamicFieldsModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    item = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ItemPhoto
        field = ('photo','caption','id')


class ItemSerializer(DynamicFieldsModelSerializer):
    photos = ItemPhotoSerializer(source='itemphoto_set', many=True, read_only=True)

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
    items   = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    service = serializers.StringRelatedField(read_only=True)
    status  = serializers.SlugRelatedField(queryset=OrderStatus.objects.all(),slug_field='title')

    class Meta:
        model = Order
        field = (Order._meta.get_all_field_names())
        exclude = ('description','created_at','updated_at')

class OrderReadSerializer(OrderSerializer):
    location_from = AddressSerializer()
    location_to = AddressSerializer()
    owner = MemberSerializer()
    assigned_to = MemberSerializer()