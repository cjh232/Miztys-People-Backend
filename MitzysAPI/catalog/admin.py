from django.contrib import admin
from .models import *

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
    list_display = ('title', 'product_id', 'date_added', 'category', 'sub_category', 'is_available')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'product', 'size', 'color', 'is_available' )

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item' )



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Order, OrderAdmin)