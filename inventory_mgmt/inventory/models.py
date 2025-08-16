from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, DecimalField, ExpressionWrapper

# Tables based on your photo (IDs & fields preserved, plus relationships)

class Brand(models.Model):  # brand_mstr 1
    brand_name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.brand_name


class Item(models.Model):  # item_mstr 2
    item_name = models.CharField(max_length=150)
    item_code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # default selling price
    #brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='items')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('item_name', 'brand')

    def __str__(self):
        return f"{self.item_name} ({self.item_code})"


class Supplier(models.Model):  # supplier_mstr 3
    supplier_name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.supplier_name


class PurchaseMaster(models.Model):  # purchase_mstr 4
    invoice_no = models.CharField(max_length=50)
    invoice_date = models.DateField()
    #supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PO #{self.invoice_no} - {self.supplier}"


class PurchaseDetail(models.Model):  # purchase_details 5
    purchase_master = models.ForeignKey(PurchaseMaster, on_delete=models.CASCADE, related_name='details')
    #item = models.ForeignKey(Item, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.amount = (self.quantity or 0) * (self.price or 0)
        super().save(*args, **kwargs)


class SaleMaster(models.Model):  # sale_mstr 6
    customer_name = models.CharField(max_length=150)
    number = models.CharField(max_length=20, blank=True)
    invoice_no = models.CharField(max_length=50)
    invoice_date = models.DateField()
    totalamount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale #{self.invoice_no} - {self.customer_name}"


class SaleDetail(models.Model):  # sale_details 7
    sale_mstr = models.ForeignKey(SaleMaster, on_delete=models.CASCADE, related_name='details')
    #item = models.ForeignKey(Item, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.amount = (self.qty or 0) * (self.price or 0)
        super().save(*args, **kwargs)


# Helper for stock computations
def item_stock_queryset():
    purchases = PurchaseDetail.objects.values('item_id').annotate(
        qty_in=Sum('quantity')
    )
    sales = SaleDetail.objects.values('item_id').annotate(
        qty_out=Sum('qty')
    )
    # Convert to dict for quick lookup
    purchases_map = {p['item_id']: p['qty_in'] or 0 for p in purchases}
    sales_map = {s['item_id']: s['qty_out'] or 0 for s in sales}
    data = []
    for item in Item.objects.select_related('brand').order_by('item_name'):
        in_qty = purchases_map.get(item.id, 0) or 0
        out_qty = sales_map.get(item.id, 0) or 0
        balance = (in_qty - out_qty)
        data.append((item, in_qty, out_qty, balance))
    return data
