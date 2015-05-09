from django.contrib import admin
from location.admin import AddressAdmin
from order.models import Order, OrderAddress, OrderBid

@admin.register(OrderAddress)
class OrderAddressAdmin(AddressAdmin):
    pass

@admin.register(OrderBid)
class OrderBidAdmin(admin.ModelAdmin):
    list_display = ('order','owner','price','remarks','accepted')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','category','title','owner','location_from','preferred_time','assigned_to','tracking_id','created_at','updated_at')

    exclude = ('status',)
