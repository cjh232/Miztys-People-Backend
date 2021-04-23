from rest_framework import serializers
from .models import *



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.category_name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.category_name')

    class Meta:
        model = Product
        fields = '__all__'


class ListItemsSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.product_id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.cat_id')

    class Meta:
        model = Item
        fields = [
            'product_id',
            'title',
            'category'
        ]