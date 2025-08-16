from django import forms
from django.forms import inlineformset_factory
from .models import Brand, Item, Supplier, PurchaseMaster, PurchaseDetail, SaleMaster, SaleDetail

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'status']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name','item_code','price','brand','status']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name','mobile_no','address','status']

class PurchaseMasterForm(forms.ModelForm):
    class Meta:
        model = PurchaseMaster
        fields = ['invoice_no','invoice_date','supplier']

class PurchaseDetailForm(forms.ModelForm):
    class Meta:
        model = PurchaseDetail
        fields = ['item','quantity','price']

PurchaseDetailFormSet = inlineformset_factory(
    PurchaseMaster, PurchaseDetail, form=PurchaseDetailForm,
    extra=1, can_delete=True
)

class SaleMasterForm(forms.ModelForm):
    class Meta:
        model = SaleMaster
        fields = ['customer_name','number','invoice_no','invoice_date']

class SaleDetailForm(forms.ModelForm):
    class Meta:
        model = SaleDetail
        fields = ['item','qty','price']

SaleDetailFormSet = inlineformset_factory(
    SaleMaster, SaleDetail, form=SaleDetailForm,
    extra=1, can_delete=True
)
