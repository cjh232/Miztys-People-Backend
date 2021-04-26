from rest_framework import serializers
from .models import *



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    brand = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Product
        fields = [
            'product_id',
            'title',
            'category_name',
            'sub_category_name',
            'brand',
            'is_available'
        ]


class ItemsSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.cat_id')


    class Meta:
        model = Item
        fields = [
            'id',
            'product_id',
            'title',
            'category',
            'size',
            'color'
        ]

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'date_added',
            'quantity',
        ]

class OrderItemSerializer(serializers.ModelSerializer):

    item = ItemsSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
