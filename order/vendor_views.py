from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
from order.models import Order, OrderBid
from order.serializers import OrderSerializer, OrderReadSerializer, OrderBidSerializer
from django.core.cache import cache
from django.http import Http404
from member.models import MemberCategory

import generic.utils as GenericUtils
from generic.views import GenericList, GenericDetails

class OrderPendingList(APIView):
    def get_orders(self, user):
        mc = MemberCategory.objects.filter(member=user, verified=True).values_list('category', flat=True)

        return Order.objects.filter(category__in=mc, accepted=False)
        # return Order.objects.filter(assigned_to=None)

    def get(self, request, format=None):
        orders = self.get_orders(request.user)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderReadSerializer(orders, many=True, exclude=('assigned_to',))
        return Response({'orders':serializedItems.data, 'count':count})

class OrderAssignedList(OrderPendingList):
    def get_orders(self, user):
        return Order.objects.filter(assigned_to=user)


class OrderDetail(APIView):
    def get_object(self, order_id, user):
        try:
            mc = MemberCategory.objects.filter(member=user, verified=True).values_list('category', flat=True)
            return Order.objects.get(id=order_id, category__in=mc)
        except:
            raise Http404

    def get(self, request, order_id, format=None):
        order = self.get_object(order_id, request.user)
        serializedOrder = OrderReadSerializer(order, exclude=('assigned_to','status'))
        return Response(serializedOrder.data)

class OrderBidDetail(APIView):
    def get_order(self, order_id, user):
        try:
            mc = MemberCategory.objects.filter(member=user, verified=True).values_list('category', flat=True)
            return Order.objects.get(id=order_id, category__in=mc)
        except:
            raise Http404

    def get_bid(self, order_id, user):
        try:
            return OrderBid.objects.get(order=order_id, owner=user)
        except:
            raise Http404

    def get(self, request, order_id):
        bid = self.get_bid(order_id, request.user)
        serializedBid = OrderBidSerializer(bid)
        return Response({'bid':serializedBid.data})

    def post(self, request, order_id):
        #to prevent the user from entering unassigned order number we override it manually
        request.data['order'] = order_id
        request.data['owner'] = request.user.id

        serializedBid = OrderBidSerializer(data=request.data)
        if serializedBid.is_valid():
            serializedBid.save(owner=request.user)
            return Response({'bid':serializedBid.data,'message':'You have successfully bid for this order'})
        return Response({'error':serializedBid.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        #to prevent the user from entering unassigned order number we override it manually
        request.data['order'] = order_id
        request.data['owner'] = request.user.id

        bid = self.get_bid(order_id, request.user)
        serializedBid = OrderBidSerializer(bid, data=request.data, partial=True)
        if serializedBid.is_valid():
            serializedBid.save()
            return Response({'bid':serializedBid.data,'message':'You have successfully change bid for this order'})
        return Response({'error':serializedBid.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = self.get_bid(order_id, request.user)
        order.delete()
        return Response({'message':'Order have been successfully deleted'}, status=status.HTTP_204_NO_CONTENT)