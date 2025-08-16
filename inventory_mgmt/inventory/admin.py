from django.contrib import admin
from .models import Brand, Item, Supplier, PurchaseMaster, PurchaseDetail, SaleMaster, SaleDetail

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 0

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 0

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name','status','datetime')
    search_fields = ('brand_name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name','item_code','brand','price','status')
    search_fields = ('item_name','item_code')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name','mobile_no','status')

@admin.register(PurchaseMaster)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','invoice_date','supplier','total_amount')
    inlines = [PurchaseDetailInline]

@admin.register(SaleMaster)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_no','invoice_date','customer_name','totalamount')
    inlines = [SaleDetailInline]
