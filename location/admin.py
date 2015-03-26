from django.contrib import admin
from location.models import Address, Area

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('gps_location','address_name','address_line_1','address_line_2','postal_code','area')

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('gps_location','area_name')