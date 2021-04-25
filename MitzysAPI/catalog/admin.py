from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *

class CustomAdminSite(AdminSite):
    site_header = "Mitzy's People Administration"

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id', 'is_child', 'parent')
    readonly_fields= ('category_id', )
    fieldsets = (
        ('Category Info', {
            "fields": (
                'name',
                'category_id',
                'parent',
                'description',
                'is_child'
            ),
        }),
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'date_added', 'category', 'sub_category', 'is_available')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'is_available' )

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'status')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart')


# admin.site = CustomAdminSite(name="myadmin")
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)