from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from location.models import Address
from location.serializers import AddressSerializer
from django.http import Http404

import generic.utils as GenericUtils
from generic.views import GenericDetails, GenericListOwner, GenericList
from django.contrib.gis.geos import GEOSGeometry

class MemberAddressList(GenericListOwner):
    Model = Address
    ModelSerializer = AddressSerializer

    def get(self, request, format=None):
        """
        Get all addresses created by this user
        ---
        serializer : location.serializers.AddressSerializer
        """

        return super(MemberAddressList, self).get(request,format)

    def post(self, request, format=None):
        """
        Create a new address
        ---
        serializer : location.serializers.AddressSerializer
        """

        serializedAddress = AddressSerializer(data=request.data)
        if serializedAddress.is_valid():
            serializedAddress.save(owner=request.user)
            return Response({'address':serializedAddress.data}, status=status.HTTP_201_CREATED)

        return Response({'error':serializedAddress.errors}, status=status.HTTP_400_BAD_REQUEST)

        


class MemberAddressDetail(GenericDetails):
    Model = Address
    ModelSerializer = AddressSerializer

    def put(self, request, address_id, format=None):
        """
        Modify an address created by this user, fields that are left empty will not be modified
        ---
        serializer : location.serializers.AddressSerializer
        """

        address = self.get_object(request.user, address_id)

        serializedAddress = AddressSerializer(address, data=request.data, partial=True)
        if serializedAddress.is_valid():
            serializedAddress.save(owner=request.user)
            return Response({'address':serializedAddress.data})

        return Response({'error':serializedAddress.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_id, format=None):
        """
        Delets this address
        ---
        omit_serializer : true
        """

        address = self.get_object(request.user, address_id)
        address.deleted = True
        address.save()
        return Response({'message':'Address successfully deleted'},status=status.HTTP_204_NO_CONTENT)


# class AreaList(GenericList):
#     Model = Area
#     ModelSerializer = AreaSerializer