from api.models import Product, Stock, VendingMachine
from django.contrib import admin

# Register your models here.


admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(VendingMachine)
