from django.contrib import admin

from .models import GoodsCategory, Brand, GoodsUnit, Store

# Register your models here.

admin.site.register(GoodsCategory)
admin.site.register(Brand)
admin.site.register(GoodsUnit)
admin.site.register(Store)
