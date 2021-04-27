from django.contrib import admin
from .models import *


# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart')
    readonly_fields = ('id',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')
    readonly_fields = ('id',)


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
