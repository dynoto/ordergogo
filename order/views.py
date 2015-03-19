from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order, Item
from order.serializers import OrderSerializer, ItemSerializer, OrderItemSerializer
import generic.utils as GenericUtils

# Create your views here.
class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(owner=request.user)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderSerializer(orders, many=True)
        return Response({'orders':serializedItems.data, 'count':count})

    def post(self, request, format=None):
        request.data['owner'] = request.user.id
        serializedOrderItemList = []
        for item in request.data['items']:
            serializedOrderItem = OrderItemSerializer(data=item)
            if serializedOrderItem.is_valid():
                serializedOrderItemList.append(serializedOrderItem)
            else:
                return Response({'message':'An error has happened while doing data validation', 'errors':serializedOrderItem.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializedOrder = OrderSerializer(data=request.data)
        if serializedOrder.is_valid():
            order = serializedOrder.save()
            for serializedOrderItem in serializedOrderItemList:
                serializedOrderItem.save(order=order)


            return Response({'message':'Order have been successfully created'}, status=status.HTTP_201_CREATED)
        return Response({'message':'An error has happened while doing data validation', 'errors':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get(self, request, format=None):
        pass


class ItemList(APIView):
    def get(self, request, format=None):
        items = Item.objects.filter(owner=request.user)
        items, count = GenericUtils.paginator(items, request.QUERY_PARAMS.get('page'))
        serializedItems = ItemSerializer(items, many=True)
        return Response({'items':serializedItems.data, 'count':count})

    def post(self, request, format=None):
        request.data['owner'] = request.user.id
        serializedItem = ItemSerializer(data=request.data)
        if serializedItem.is_valid():
            serializedItem.save()
            return Response(serializedItem.data, status=status.HTTP_201_CREATED)
        return Response(serializedItem.errors, status=status.HTTP_400_BAD_REQUEST)

        


class ItemDetail(APIView):
    def get(self, request, item_id, format=None):
        item = Item.objects.get(owner=request.user, id=item_id)
        serializedItem = ItemSerializer(item)
        return Response(serializedItem.data)