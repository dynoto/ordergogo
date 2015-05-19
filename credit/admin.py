from django.contrib import admin
from credit.models import Package, Transaction

# Register your models here.


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title','description','price','credits')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('package','member','amount','transaction_id')