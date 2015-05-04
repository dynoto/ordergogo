# from generic.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from location.models import Address, Area

class AddressSerializer(GeoModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        geo_field = "gps_location"
        fields = (Address._meta.get_all_field_names())
        exclude = ('created_at','updated_at','owner')



class AreaSerializer(GeoModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Area
        geo_field = "gps_location"
        fields = (Area._meta.get_all_field_names())

