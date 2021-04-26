from django.contrib import admin
from .models import *
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart')
    readonly_fields= ('id', )

admin.site.register(CartItem, CartItemAdmin)
