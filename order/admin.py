from django.contrib import admin
from order.models import Order, OrderItem, OrderStatus, ServiceType, Item, ItemPhoto
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class ItemPhotoInline(admin.StackedInline):
    model = ItemPhoto

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','title','owner','assigned_to','created_at','updated_at')
    inlines = [OrderItemInline]

    exclude = ('owner','description')

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    exclude = ('owner',)
    list_display = ('id','title','price','created_at','updated_at')
    inlines = [ItemPhotoInline]

    def get_queryset(self, request):
        qs = super(ItemAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','item','order_price','quantity','remarks')

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('id','title')

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('id','title')


@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('id','item','photo','caption','created_at','updated_at')
    exclude = ('owner',)

    def get_queryset(self, request):
        qs = super(ItemPhotoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()