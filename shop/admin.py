from django.contrib import admin
from .models import *


# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified', 'phone', 'email')


admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopImages)
admin.site.register(ProductImages)
admin.site.register(Description)
admin.site.register(About)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(CartItem)
