from django.contrib import admin
from .models import Vendor, Supplier, Product, Order

admin.site.register(Vendor)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order)
