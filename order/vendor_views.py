from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
from order.models import Order
from order.serializers import OrderSerializer, OrderReadSerializer, OrderBidSerializer
from django.core.cache import cache
from django.http import Http404

import generic.utils as GenericUtils
from generic.views import GenericList, GenericDetails

class OrderPendingList(APIView):
    def get_orders(user):
        return Order.objects.filter(category=user.category, assigned_to=None)

    def get(self, request, format=None):
        orders = self.get_orders(request.user)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderReadSerializer(orders, many=True)
        return Response({'orders':serializedItems.data, 'count':count})

class OrderAssignedList(OrderPendingList):
    def get_orders(user):
        return Order.objects.filter(assigned_to=user)


class OrderDetail(APIView):
    def get_object(order_id, user):
        try:
            return Order.objects.get(id=order_id, category=user.category)
        except:
            return Http404

    def get(self, request, order_id, format=None):
        order = self.get_object(order_id, request.user)
        serializedOrder = OrderReadSerializer(order)
        return Response(serializedOrder.data)

    def post(self, request, order_id):
        serializedBid = OrderBidSerializer(data=request.data)
        if serializedBid.is_valid():
            serializedBid.save()