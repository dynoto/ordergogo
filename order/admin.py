from django.contrib import admin
from order.models import Order

# @admin.register(OrderAddress)
# class OrderAddressAdmin(AddressAdmin):
#     pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','assigned_to','created_at','updated_at')

    exclude = ('status',)