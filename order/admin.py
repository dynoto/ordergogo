from django.contrib import admin
from order.models import Order, OrderItem, Item, ItemPhoto
class OrderItemInline(admin.TabularInline):
    model = OrderItem


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','assigned_to','created_at','updated_at')
    inlines = [OrderItemInline]

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id','title','price','created_at','updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','item','order_price','quantity','remarks')


@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('item','caption','created_at','updated_at')