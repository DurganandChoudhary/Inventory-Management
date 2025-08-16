# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.db import transaction
# from django.db.models import Sum, Q
# from django.utils import timezone
# from .models import (
#     Brand, Item, Supplier,
#     PurchaseMaster, PurchaseDetail,
#     SaleMaster, SaleDetail,
#     item_stock_queryset
# )
# from .forms import (
#     BrandForm, ItemForm, SupplierForm,
#     PurchaseMasterForm, PurchaseDetailFormSet,
#     SaleMasterForm, SaleDetailFormSet
# )

# def dashboard(request):
#     return render(request, 'inventory/dashboard.html', {
#         'brand_count': Brand.objects.count(),
#         'item_count': Item.objects.count(),
#         'supplier_count': Supplier.objects.count(),
#         'purchase_count': PurchaseMaster.objects.count(),
#         'sale_count': SaleMaster.objects.count(),
#     })


# # ---------- Brand CRUD ----------
# def brand_list(request):
#     q = request.GET.get('q','')
#     brands = Brand.objects.all().order_by('brand_name')
#     if q:
#         brands = brands.filter(brand_name__icontains=q)
#     return render(request, 'inventory/brand_list.html', {'brands': brands, 'q': q})

# def brand_create(request):
#     form = BrandForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Brand created.')
#         return redirect('brand_list')
#     return render(request, 'inventory/brand_form.html', {'form': form})

# def brand_update(request, pk):
#     obj = get_object_or_404(Brand, pk=pk)
#     form = BrandForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Brand updated.')
#         return redirect('brand_list')
#     return render(request, 'inventory/brand_form.html', {'form': form})

# def brand_delete(request, pk):
#     obj = get_object_or_404(Brand, pk=pk)
#     obj.delete()
#     messages.success(request, 'Brand deleted.')
#     return redirect('brand_list')


# # ---------- Item CRUD ----------
# def item_list(request):
#     q = request.GET.get('q','')
#     items = Item.objects.select_related('brand').order_by('item_name')
#     if q:
#         items = items.filter(Q(item_name__icontains=q)|Q(item_code__icontains=q))
#     return render(request, 'inventory/item_list.html', {'items': items, 'q': q})

# def item_create(request):
#     form = ItemForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Item created.')
#         return redirect('item_list')
#     return render(request, 'inventory/item_form.html', {'form': form})

# def item_update(request, pk):
#     obj = get_object_or_404(Item, pk=pk)
#     form = ItemForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Item updated.')
#         return redirect('item_list')
#     return render(request, 'inventory/item_form.html', {'form': form})

# def item_delete(request, pk):
#     obj = get_object_or_404(Item, pk=pk)
#     obj.delete()
#     messages.success(request, 'Item deleted.')
#     return redirect('item_list')


# # ---------- Supplier CRUD ----------
# def supplier_list(request):
#     q = request.GET.get('q','')
#     suppliers = Supplier.objects.all().order_by('supplier_name')
#     if q:
#         suppliers = suppliers.filter(supplier_name__icontains=q)
#     return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers, 'q': q})

# def supplier_create(request):
#     form = SupplierForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Supplier created.')
#         return redirect('supplier_list')
#     return render(request, 'inventory/supplier_form.html', {'form': form})

# def supplier_update(request, pk):
#     obj = get_object_or_404(Supplier, pk=pk)
#     form = SupplierForm(request.POST or None, instance=obj)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Supplier updated.')
#         return redirect('supplier_list')
#     return render(request, 'inventory/supplier_form.html', {'form': form})

# def supplier_delete(request, pk):
#     obj = get_object_or_404(Supplier, pk=pk)
#     obj.delete()
#     messages.success(request, 'Supplier deleted.')
#     return redirect('supplier_list')


# # ---------- Purchases ----------
# @transaction.atomic
# def purchase_create(request):
#     m_form = PurchaseMasterForm(request.POST or None)
#     formset = PurchaseDetailFormSet(request.POST or None)
#     if request.method == 'POST':
#         if m_form.is_valid() and formset.is_valid():
#             master = m_form.save()
#             total = 0
#             details = formset.save(commit=False)
#             for d in details:
#                 d.purchase_master = master
#                 d.save()
#                 total += d.amount
#             master.total_amount = total
#             master.save()
#             messages.success(request, 'Purchase saved.')
#             return redirect('purchase_detail', pk=master.pk)
#     return render(request, 'inventory/purchase_form.html', {'m_form': m_form, 'formset': formset})

# def purchase_list(request):
#     q = request.GET.get('q', '')
#     objs = PurchaseMaster.objects.select_related('supplier').order_by('-invoice_date','-id')
#     if q:
#         objs = objs.filter(Q(invoice_no__icontains=q)|Q(supplier__supplier_name__icontains=q))
#     return render(request, 'inventory/purchase_list.html', {'objects': objs, 'q': q})

# def purchase_detail(request, pk):
#     obj = get_object_or_404(PurchaseMaster, pk=pk)
#     return render(request, 'inventory/purchase_detail.html', {'obj': obj})


# # ---------- Sales ----------
# @transaction.atomic
# def sale_create(request):
#     m_form = SaleMasterForm(request.POST or None)
#     formset = SaleDetailFormSet(request.POST or None)
#     if request.method == 'POST':
#         if m_form.is_valid() and formset.is_valid():
#             master = m_form.save()
#             total = 0
#             details = formset.save(commit=False)
#             for d in details:
#                 d.sale_mstr = master
#                 # Validate stock (simple)
#                 purchased = PurchaseDetail.objects.filter(item=d.item).aggregate(q=Sum('quantity'))['q'] or 0
#                 sold = SaleDetail.objects.filter(item=d.item).aggregate(q=Sum('qty'))['q'] or 0
#                 available = purchased - sold
#                 if d.qty > available:
#                     transaction.set_rollback(True)
#                     messages.error(request, f"Insufficient stock for {d.item}. Available: {available}")
#                     return render(request, 'inventory/sale_form.html', {'m_form': m_form, 'formset': formset})
#                 d.save()
#                 total += d.amount
#             master.totalamount = total
#             master.save()
#             messages.success(request, 'Sale saved.')
#             return redirect('sale_detail', pk=master.pk)
#     return render(request, 'inventory/sale_form.html', {'m_form': m_form, 'formset': formset})

# def sale_list(request):
#     q = request.GET.get('q', '')
#     objs = SaleMaster.objects.order_by('-invoice_date','-id')
#     if q:
#         objs = objs.filter(Q(invoice_no__icontains=q)|Q(customer_name__icontains=q))
#     return render(request, 'inventory/sale_list.html', {'objects': objs, 'q': q})

# def sale_detail(request, pk):
#     obj = get_object_or_404(SaleMaster, pk=pk)
#     return render(request, 'inventory/sale_detail.html', {'obj': obj})


# # ---------- Reports ----------
# def report_stock(request):
#     rows = item_stock_queryset()  # list of tuples (item, in, out, balance)
#     q = request.GET.get('q','')
#     if q:
#         rows = [r for r in rows if (q.lower() in r[0].item_name.lower() or q.lower() in r[0].item_code.lower())]
#     return render(request, 'inventory/report_stock.html', {'rows': rows, 'q': q})

# def report_purchase(request):
#     date_from = request.GET.get('from')
#     date_to = request.GET.get('to')
#     item_id = request.GET.get('item')
#     qs = PurchaseDetail.objects.select_related('purchase_master','item')
#     if date_from:
#         qs = qs.filter(purchase_master__invoice_date__gte=date_from)
#     if date_to:
#         qs = qs.filter(purchase_master__invoice_date__lte=date_to)
#     if item_id:
#         qs = qs.filter(item_id=item_id)
#     items = Item.objects.order_by('item_name')
#     total = qs.aggregate(s=Sum('amount'))['s'] or 0
#     return render(request, 'inventory/report_purchase.html', {
#         'rows': qs.order_by('purchase_master__invoice_date'),
#         'items': items,
#         'date_from': date_from,
#         'date_to': date_to,
#         'item_id': int(item_id) if item_id else None,
#         'total': total
#     })

# def report_sale(request):
#     date_from = request.GET.get('from')
#     date_to = request.GET.get('to')
#     item_id = request.GET.get('item')
#     qs = SaleDetail.objects.select_related('sale_mstr','item')
#     if date_from:
#         qs = qs.filter(sale_mstr__invoice_date__gte=date_from)
#     if date_to:
#         qs = qs.filter(sale_mstr__invoice_date__lte=date_to)
#     if item_id:
#         qs = qs.filter(item_id=item_id)
#     items = Item.objects.order_by('item_name')
#     total = qs.aggregate(s=Sum('amount'))['s'] or 0
#     return render(request, 'inventory/report_sale.html', {
#         'rows': qs.order_by('sale_mstr__invoice_date'),
#         'items': items,
#         'date_from': date_from,
#         'date_to': date_to,
#         'item_id': int(item_id) if item_id else None,
#         'total': total
#     })

















from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date

from .models import (
    Brand, Item, Supplier,
    PurchaseMaster, PurchaseDetail,
    SaleMaster, SaleDetail,
    item_stock_queryset
)
from .forms import (
    BrandForm, ItemForm, SupplierForm,
    PurchaseMasterForm, PurchaseDetailFormSet,
    SaleMasterForm, SaleDetailFormSet
)


def dashboard(request):
    return render(request, 'inventory/dashboard.html', {
        'brand_count': Brand.objects.count(),
        'item_count': Item.objects.count(),
        'supplier_count': Supplier.objects.count(),
        'purchase_count': PurchaseMaster.objects.count(),
        'sale_count': SaleMaster.objects.count(),
    })


# ---------- Brand CRUD ----------
def brand_list(request):
    q = request.GET.get('q','')
    brands = Brand.objects.all().order_by('brand_name')
    if q:
        brands = brands.filter(brand_name__icontains=q)
    return render(request, 'inventory/brand_list.html', {'brands': brands, 'q': q})

def brand_create(request):
    form = BrandForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Brand created.')
        return redirect('brand_list')
    return render(request, 'inventory/brand_form.html', {'form': form})

def brand_update(request, pk):
    obj = get_object_or_404(Brand, pk=pk)
    form = BrandForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Brand updated.')
        return redirect('brand_list')
    return render(request, 'inventory/brand_form.html', {'form': form})

def brand_delete(request, pk):
    obj = get_object_or_404(Brand, pk=pk)
    obj.delete()
    messages.success(request, 'Brand deleted.')
    return redirect('brand_list')


# ---------- Item CRUD ----------
def item_list(request):
    q = request.GET.get('q','')
    items = Item.objects.select_related('brand').order_by('item_name')
    if q:
        items = items.filter(Q(item_name__icontains=q)|Q(item_code__icontains=q))
    return render(request, 'inventory/item_list.html', {'items': items, 'q': q})

def item_create(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item created.')
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

def item_update(request, pk):
    obj = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Item updated.')
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

def item_delete(request, pk):
    obj = get_object_or_404(Item, pk=pk)
    obj.delete()
    messages.success(request, 'Item deleted.')
    return redirect('item_list')


# ---------- Supplier CRUD ----------
def supplier_list(request):
    q = request.GET.get('q','')
    suppliers = Supplier.objects.all().order_by('supplier_name')
    if q:
        suppliers = suppliers.filter(supplier_name__icontains=q)
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers, 'q': q})

def supplier_create(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier created.')
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_update(request, pk):
    obj = get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Supplier updated.')
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_form.html', {'form': form})

def supplier_delete(request, pk):
    obj = get_object_or_404(Supplier, pk=pk)
    obj.delete()
    messages.success(request, 'Supplier deleted.')
    return redirect('supplier_list')


# ---------- Purchases ----------
@transaction.atomic
def purchase_create(request):
    m_form = PurchaseMasterForm(request.POST or None)
    formset = PurchaseDetailFormSet(request.POST or None)
    today = date.today()
    if request.method == 'POST':
        if m_form.is_valid() and formset.is_valid():
            master = m_form.save()
            total = 0
            details = formset.save(commit=False)
            for d in details:
                d.purchase_master = master
                d.save()
                total += d.amount
            master.total_amount = total
            master.save()
            messages.success(request, 'Purchase saved.')
            return redirect('purchase_detail', pk=master.pk)
    return render(request, 'inventory/purchase_form.html', {
        'm_form': m_form,
        'formset': formset,
        'today_date': today
    })

def purchase_list(request):
    q = request.GET.get('q', '')
    objs = PurchaseMaster.objects.select_related('supplier').order_by('-invoice_date','-id')
    if q:
        objs = objs.filter(Q(invoice_no__icontains=q)|Q(supplier__supplier_name__icontains=q))
    return render(request, 'inventory/purchase_list.html', {'objects': objs, 'q': q})

def purchase_detail(request, pk):
    obj = get_object_or_404(PurchaseMaster, pk=pk)
    return render(request, 'inventory/purchase_detail.html', {'obj': obj})


# ---------- Sales ----------
@transaction.atomic
def sale_create(request):
    m_form = SaleMasterForm(request.POST or None)
    formset = SaleDetailFormSet(request.POST or None)
    today = date.today()
    if request.method == 'POST':
        if m_form.is_valid() and formset.is_valid():
            master = m_form.save()
            total = 0
            details = formset.save(commit=False)
            for d in details:
                d.sale_mstr = master
                purchased = PurchaseDetail.objects.filter(item=d.item).aggregate(q=Sum('quantity'))['q'] or 0
                sold = SaleDetail.objects.filter(item=d.item).aggregate(q=Sum('qty'))['q'] or 0
                available = purchased - sold
                if d.qty > available:
                    transaction.set_rollback(True)
                    messages.error(request, f"Insufficient stock for {d.item}. Available: {available}")
                    return render(request, 'inventory/sale_form.html', {
                        'm_form': m_form,
                        'formset': formset,
                        'today_date': today
                    })
                d.save()
                total += d.amount
            master.totalamount = total
            master.save()
            messages.success(request, 'Sale saved.')
            return redirect('sale_detail', pk=master.pk)
    return render(request, 'inventory/sale_form.html', {
        'm_form': m_form,
        'formset': formset,
        'today_date': today
    })

def sale_list(request):
    q = request.GET.get('q', '')
    objs = SaleMaster.objects.order_by('-invoice_date','-id')
    if q:
        objs = objs.filter(Q(invoice_no__icontains=q)|Q(customer_name__icontains=q))
    return render(request, 'inventory/sale_list.html', {'objects': objs, 'q': q})

def sale_detail(request, pk):
    obj = get_object_or_404(SaleMaster, pk=pk)
    return render(request, 'inventory/sale_detail.html', {'obj': obj})


# ---------- Reports ----------
def report_stock(request):
    rows = item_stock_queryset()
    q = request.GET.get('q','')
    if q:
        rows = [r for r in rows if (q.lower() in r[0].item_name.lower() or q.lower() in r[0].item_code.lower())]
    return render(request, 'inventory/report_stock.html', {'rows': rows, 'q': q})

def report_purchase(request):
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    item_id = request.GET.get('item')
    qs = PurchaseDetail.objects.select_related('purchase_master','item')
    if date_from:
        qs = qs.filter(purchase_master__invoice_date__gte=date_from)
    if date_to:
        qs = qs.filter(purchase_master__invoice_date__lte=date_to)
    if item_id:
        qs = qs.filter(item_id=item_id)
    items = Item.objects.order_by('item_name')
    total = qs.aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'inventory/report_purchase.html', {
        'rows': qs.order_by('purchase_master__invoice_date'),
        'items': items,
        'date_from': date_from,
        'date_to': date_to,
        'item_id': int(item_id) if item_id else None,
        'total': total
    })

def report_sale(request):
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    item_id = request.GET.get('item')
    qs = SaleDetail.objects.select_related('sale_mstr','item')
    if date_from:
        qs = qs.filter(sale_mstr__invoice_date__gte=date_from)
    if date_to:
        qs = qs.filter(sale_mstr__invoice_date__lte=date_to)
    if item_id:
        qs = qs.filter(item_id=item_id)
    items = Item.objects.order_by('item_name')
    total = qs.aggregate(s=Sum('amount'))['s'] or 0
    return render(request, 'inventory/report_sale.html', {
        'rows': qs.order_by('sale_mstr__invoice_date'),
        'items': items,
        'date_from': date_from,
        'date_to': date_to,
        'item_id': int(item_id) if item_id else None,
        'total': total
    })
