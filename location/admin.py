from django.contrib import admin
from location.models import Address, Area

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_name','address_line_1','address_line_2','postal_code','area','gps_location','owner')

    # def get_queryset(self, request):
    #     qs = super(AddressAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(owner=request.user)

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     obj.save()

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('area_name','gps_location','owner')
    exclude = ('owner',)