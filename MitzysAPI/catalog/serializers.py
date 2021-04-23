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


class ListItemsSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.product_id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.cat_id')


    class Meta:
        model = Item
        fields = [
            'product_id',
            'title',
            'category',

        ]