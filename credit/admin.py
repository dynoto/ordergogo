from django.contrib import admin
from credit.models import Package, Transaction

# Register your models here.


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id','title','description','price','credit')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id','package','member','amount','transaction_id','is_paypal','is_apple','is_google')