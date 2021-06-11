from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent', 'breadcrumb', 'products_count')
    empty_value_display = '...'
    search_fields = ('name', 'desc')
    list_filter = ('parent',  )
    readonly_fields= ('id', 'products_count')
    fieldsets = (
        ('Details:', {
            "fields": (
                'name',
                'desc',
            ),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Meta:', {
            "fields": (
                'id',
                'parent',
                'products_count'
            ),
            'classes': ('collapse', 'extrapretty'),
        })
    )

def make_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)

def make_available(modeladmin, request, queryset):
    queryset.update(is_available=True)

make_unavailable.short_description = "Mark product(s) unavailable."
make_available.short_description = "Mark product(s) available."

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'date_added', 'category', 'sub_category', 'is_available')
    search_fields = ('title', 'brand')
    list_display_links = ('title', 'id')
    list_filter = ('is_available', 'brand', 'category' )
    prepopulated_fields = {"slug": ("title",)}

    actions = [make_unavailable, make_available]

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'quantity', 'brand', 'category', 'sub_category')
    list_filter = ('product__brand', 'size__type' )
    search_fields = ('product__title', 'product__details')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'products_count')
    readonly_fields= ('id', 'products_count')
    list_display_links = ('name', )

    fieldsets = (
        ('Brand Info', {
            "fields": (
                'name',
                'id',
                'products_count',
            ),
        }),
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'date_added')
    readonly_fields= ('date_added', )
    list_filter = ('type',  )
    fieldsets = (
        ('Size Info', {
            "fields": (
                'type',
                'value',
                'date_added',
            ),
        }),
    )

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')



