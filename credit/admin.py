from django.contrib import admin
from credit.models import Credit, Package, Transaction

# Register your models here.
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('member','credits')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title','description','price','credits')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('package','credit','transaction_id')