from django.contrib import admin
from location.models import Address

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('gps_location',)