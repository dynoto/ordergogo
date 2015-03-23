from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order, Item
from order.serializers import OrderSerializer, OrderReadSerializer, ItemSerializer, OrderItemSerializer
import generic.utils as GenericUtils
from django.core.cache import cache

# Create your views here.
class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(owner=request.user)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderReadSerializer(orders, many=True)
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
    def get(self, request, order_id, format=None):
        try:
            order = Order.objects.get(owner=request.user, id=order_id)
            serializedOrder = OrderSerializer(order)
            return Response(serializedOrder.data)
        except:
            return Response({'message':'You are not authorized to modify this order'})

class OrderAssign(APIView):
    def post(self, request, order_id, format=None):
        try:
            order = Order.objects.get(owner=request.user, id=order_id)
        except:
            return Response({'message':'You are not authorized to modify this order'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order.assigned_to = request.data['assigned_to']
            order.save()
        except:
            return Response({'message':'Failed to assign driver, check whether that guy exist or not'}, status=status.HTTP_400_BAD_REQUEST)    

        message = 'Order successfully assign to : %s %s' %(order.assigned_to.first_name, order.assigned_to.last_name)
        return Response({'message':message})


class OrderTrack(APIView):
    def get(self, request, tracking_id, format=None):
        gps_position = cache.get(tracking_id)
        return Response(gps_position)

    def post(self, request, tracking_id, format=None):
        cache.set(tracking_id,request.data['gps_position'])
        return Response({'message':'Driver position updated'})



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