# from generic.serializers import DynamicFieldsModelSerializer
# from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from location.models import Address, Area

class AddressSerializer(GeoModelSerializer):
    class Meta:
        model = Address
        geo_field = "gps_location"
        fields = ('id','address_name','address_line_1','address_line_2','postal_code','area','gps_location','created_at','updated_at')
        extra_kwargs = {
            'owner':{'read_only':True}
        }



class AreaSerializer(GeoModelSerializer):
    class Meta:
        model = Area
        geo_field = "gps_location"
        fields = (Area._meta.get_all_field_names())
        extra_kwargs = {
            'owner':{'read_only':True}
        }