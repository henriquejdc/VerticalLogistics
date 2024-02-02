# Django imports
from django.contrib import admin

# Project imports
from .models import UserVL, Order, Product


admin.site.register(UserVL)
admin.site.register(Order)
admin.site.register(Product)
