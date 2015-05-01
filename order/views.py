from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
from order.models import Order, Item, ItemPhoto, OrderStatus, ServiceType
from order.serializers import OrderSerializer, OrderReadSerializer, ItemSerializer, OrderItemSerializer, ItemPhotoSerializer, ServiceTypeSerializer, OrderStatusSerializer
from django.core.cache import cache
from django.http import Http404

import generic.utils as GenericUtils
from generic.views import GenericList, GenericDetails

# Create your views here.
class OrderList(APIView):
    def get(self, request, format=None):
        orders = Order.objects.filter(assigned_to=request.user)
        orders, count = GenericUtils.paginator(orders, request.QUERY_PARAMS.get('page'))
        serializedItems = OrderReadSerializer(orders, many=True, exclude=('owner','assigned_to'))
        return Response({'orders':serializedItems.data, 'count':count})
        

    def post(self, request, format=None):
        serializedOrder = OrderSerializer(data=request.data,exclude=('status','owner','assigned_to'))
        if serializedOrder.is_valid():
            serializedOrder.save(owner=request.user)
            return Response({'message':'Order have been successfully created'}, status=status.HTTP_201_CREATED)
        return Response({'message':'An error has happened while doing data validation', 'errors':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)



class OrderDetail(APIView):
    def get_object(order_id, owner):
        try:
            return Order.objects.get(id=order_id, owner=owner)
        except:
            return Http404


    def get(self, request, order_id, format=None):
        order = self.get_object(id=order_id, owner=request.user)
        serializedOrder = OrderReadSerializer(order)
        return Response(serializedOrder.data)

    def put(self, request, order_id, format=None):
        order = self.get_object(id=order_id, owner=request.user)
        serializedOrder = OrderSerializer(order, data=request.data, exclude=('status','owner','assigned_to'))
        if serializedOrder.is_valid():
            serializedOrder.save()
            return Response({'message':'Order have been successfully created','order':serializedOrder.data}, status=status.HTTP_200_CREATED)
        else:
            return Response({'message':'An error has happened while doing data validation', 'errors':serializedOrder.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = self.get_object(id=order_id, owner=request.user)
        order.delete()
        return Response({'message':'Order have been successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class OrderAccept(APIView):
    def post(self, request, order_id, format=None):
        order = Order.objects.get_order_from_owner(order_id, request.user)
        serializedOrder = OrderSerializer(order, data=request.data, fields=)

# class OrderStatusChange(APIView):
#     def put(self, request, order_id, format=None):
#         try:
#             order = Order.objects.get_assigned_order(request.user, order_id)
#         except:
#             return Response({'message':'You are not authorized to modify this order'}, status=status.HTTP_400_BAD_REQUEST)

#         serializedOrder = OrderSerializer(order, data=request.data, exclude=('location_to','owner','location_from','title','items','service','description','remarks'))
#         if serializedOrder.is_valid():
#             serializedOrder.save()
#             return Response(serializedOrder.data)
#         return Response(serializedOrder.errors, status=status.HTTP_400_BAD_REQUEST)

# class OrderReject(APIView):
#     def put(self, request, order_id, format=None):
#         try:
#             order = Order.objects.get_assigned_order(request.user, order_id)
#         except:
#             return Response({'message':'You are not authorized to modify this order'}, status=status.HTTP_400_BAD_REQUEST)

#         order.assigned_to = None
#         try:
#             order.save()
#             return Response({'message':'Reject order success'})
#         except:
#             return Response({'message':'Something is wrong when cancelling order'}, status=status.HTTP_400_BAD_REQUEST)

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

    def put(self, request, tracking_id, format=None):
        cache.set(tracking_id,request.data['gps_position'])
        return Response({'message':'Driver position updated'})



# class ItemList(GenericList):
#     Model = Item
#     ModelSerializer = ItemSerializer

#     def post(self, request, format=None):
#         request.data['owner'] = request.user.id
#         serializedItem = ItemSerializer(data=request.data)
#         if serializedItem.is_valid():
#             serializedItem.save()
#             return Response(serializedItem.data, status=status.HTTP_201_CREATED)
#         return Response(serializedItem.errors, status=status.HTTP_400_BAD_REQUEST)

        


# class ItemDetail(GenericDetails):
#     Model = Item
#     ModelSerializer = ItemSerializer

#     def get_object(self, user, model_id):
#         try:
#             return self.Model.objects.get(assigned_to=user, id=model_id)
#         except:
#             raise Http404

#     def delete(self, request, model_id, format=None):
#         return Response({'error':'You cannot delete this item'}, status=status.HTTP_400_BAD_REQUEST)


# class PhotoList(GenericList):
#     Model = ItemPhoto
#     ModelSerializer = ItemPhotoSerializer
#     # parser_classes = (MultiPartParser,)

#     def post(self, request, item_id, format=None):
#         # CONTENT-TYPE : multipart/form-data; boundary=----
#         try:
#             item = Item.objects.get(owner=request.user, id=item_id)
#         except:
#             raise Http404

        
#         if item.owner == request.user:
#             serializedItemPhoto = self.ModelSerializer(data=request.data)
#             if serializedItemPhoto.is_valid():
#                 serializedItemPhoto.save(item=item, owner=item.owner)        
#                 return Response(serializedItemPhoto.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializedItemPhoto.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'message':'You are not authorized to modify this order'}, status=status.HTTP_401_UNAUTHORIZED)

# class ServiceTypeList(APIView):
#     def get(self, request, format=None):
#         objects = ServiceType.objects.all()
#         serializedObjects = ServiceTypeSerializer(objects, many=True, exclude=('owner',))
#         return Response({'service_types':serializedObjects.data})

# class OrderStatusList(APIView):
#     def get(self, request, format=None):
#         objects = OrderStatus.objects.all()
#         serializedObjects = OrderStatusSerializer(objects, many=True, exclude=('owner',))
#         return Response({'order_statuses':serializedObjects.data})