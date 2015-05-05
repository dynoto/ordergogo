from django.contrib import admin
from order.models import Order, OrderAddress
from location.admin import AddressAdmin

@admin.register(OrderAddress)
class OrderAddressAdmin(AddressAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','assigned_to','created_at','updated_at')

    exclude = ('status',)

    # def get_queryset(self, request):
    #     qs = super(OrderAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(owner=request.user)

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     obj.save()