from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
from order.models import Order, OrderBid
from order.serializers import OrderSerializer, OrderReadSerializer, OrderBidSerializer, OrderAssignSerializer
# from django.core.cache import cache
from django.http import Http404

import generic.utils as GenericUtils
# from generic.views import GenericList, GenericDetails

# Create your views here.
class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(owner=request.user, deleted=False)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderReadSerializer(orders, many=True, exclude=('owner',))
        return Response({'orders':serializedItems.data, 'count':count})
        

    def post(self, request, format=None):
        serializedOrder = OrderSerializer(data=request.data,exclude=('status','owner','assigned_to'))
        if serializedOrder.is_valid():
            serializedOrder.save(owner=request.user)
            return Response({'order':serializedOrder.data}, status=status.HTTP_201_CREATED)
        return Response({'error':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get_object(self, order_id, owner):
        try:
            return Order.objects.get(id=order_id, owner=owner, deleted=False)
        except:
            raise Http404


    def get(self, request, order_id, format=None):
        order = self.get_object(order_id, request.user)
        serializedOrder = OrderReadSerializer(order)
        return Response({'order':serializedOrder.data})

    def put(self, request, order_id, format=None):
        order = self.get_object(id=order_id, owner=request.user)
        serializedOrder = OrderSerializer(order, data=request.data, exclude=('status','owner','assigned_to'))
        if serializedOrder.is_valid():
            serializedOrder.save()
            return Response({'order':serializedOrder.data}, status=status.HTTP_200_CREATED)
        else:
            return Response({'error':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = self.get_object(order_id, request.user)
        order.deleted = True
        order.save()
        return Response({'message':'Order have been successfully deleted'}, status=status.HTTP_204_NO_CONTENT)



class OrderAssign(APIView):
    def get_order(self, id, owner):
        try:
            return Order.objects.get(id=id, owner=owner, deleted=False)
        except:
            raise Http404

    def get(self, request, order_id, format=None):
        order = self.get_order(order_id, request.user)
        bidders = OrderBid.objects.filter(order=order)
        bidders, count = GenericUtils.paginator(bidders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderBidSerializer(bidders, many=True)
        return Response({'bid':serializedItems.data, 'count':count})


    def post(self, request, order_id, format=None):
        order = self.get_order(order_id, request.user)
        try:
            request.data['assigned_to']
        except:
            return Response({'error':{'assigned_to':['Please assign to a vendor']}}, status=status.HTTP_400_BAD_REQUEST)    

        serializedOrder = OrderAssignSerializer(order, data=request.data)
        if serializedOrder.is_valid():
            serializedOrder.save(accepted=True)
            message = 'Order successfully assign to %s %s' %(order.assigned_to.first_name, order.assigned_to.last_name)
            return Response({'message':message})

        else:
            return Response({'error':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)    

