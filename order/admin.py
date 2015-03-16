from django.contrib import admin
from order.models import Order, Item, ItemPhoto

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('reference_number','title','created_by','assigned_to','created_at','updated_at')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title','price','created_at','updated_at')

@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('item','caption','created_at','updated_at')