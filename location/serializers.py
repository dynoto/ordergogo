# from generic.serializers import DynamicFieldsModelSerializer
from rest_framework_gis.serializers import GeoModelSerializer
from location.models import Address

class AddressSerializer(GeoModelSerializer):
    class Meta:
        model = Address
        geo_field = "gps_location"
        field = (Address._meta.get_all_field_names())

