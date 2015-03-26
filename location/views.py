from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from location.models import Address
from location.serializers import AddressSerializer
import generic.utils as GenericUtils
from django.http import Http404
# from django.contrib.gis.geos import GEOSGeometry

class AddressList(APIView):
    def get(self, request, format=None):
        addresses = Address.objects.filter(owner=request.user)
        addresses, count = GenericUtils.paginator(addresses, request.QUERY_PARAMS.get('page'))
        serializedAddresses = AddressSerializer(addresses, many=True)
        return Response({'addresses':serializedAddresses.data, 'count':count})

    def post(self, request, format=None):
        serializedAddress = AddressSerializer(data=request.data)
        if serializedAddress.is_valid():
            # gps_data = request.data['gps_location']
            # gps_location = GEOSGeometry('POINT(%s %s)' % (gps_data['lat'], gps_data['lon']))

            serializedAddress.save(owner=request.user)
            return Response(serializedAddress.data, status=status.HTTP_201_CREATED)
        return Response(serializedAddress.errors, status=status.HTTP_400_BAD_REQUEST)

        


class AddressDetail(APIView):
    def get_object(self, user, Address_id):
        try:
            return Address.objects.get(owner=user, id=Address_id)
        except:
            raise Http404

    def get(self, request, Address_id, format=None):
        serializedAddress = AddressSerializer(self.get_object(request.user, Address_id))
        return Response(serializedAddress.data)

    def put(self, request, Address_id, format=None):
        address = self.get_object(request.user, Address_id)

        serializedAddress = AddressSerializer(address, data=request.data)
        if serializedAddress.is_valid():
            serializedAddress.save(owner=request.user)
            return Response(serializedAddress.data)
        return Response(serializedAddress.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, Address_id, format=None):
        address = self.get_object(request.user, Address_id)
        try:
            address.delete()
            return Response({'message':'Address deleted successfully'})
        except:
            return Response({'error':'Address cannot be deleted because it is still associated with order(s)'}, status=status.HTTP_400_BAD_REQUEST)


