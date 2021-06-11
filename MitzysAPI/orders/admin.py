from django.contrib import admin
from .models import *


# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order')
    readonly_fields = ('id',)


admin.site.register(OrderItem, OrderItemAdmin)

