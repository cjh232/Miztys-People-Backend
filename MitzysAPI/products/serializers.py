from rest_framework import serializers
from .models import *

class VariantSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.cat_id')


    class Meta:
        model = Variant
        fields = [
            'id',
            'product_id',
            'title',
            'category',
            'size',
            'color'
        ]

class VariantListSerializer(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    category = serializers.ReadOnlyField(source='product.category.cat_id')
    # size = serializers.ReadOnlyField(source='size.value')
    # color = serializers.ReadOnlyField(source='color.name')


    class Meta:
        model = Variant
        fields = [
            'product_id',
            'title',
            'category',
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    brand = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'category_name',
            'sub_category_name',
            'brand',
            'is_available',
            'details',
        ]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    sub_category_name = serializers.ReadOnlyField(source='sub_category.name')
    brand = serializers.ReadOnlyField(source='brand.name')

    # variants = VariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'category_name',
            'sub_category_name',
            'brand',
            'is_available',
            'details',
            'available_colors'
        ]

class BrandListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields ='__all__'

class SizeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields ='__all__'

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'name',
            'id',
            'desc',
            'breadcrumb'    
        ]

class CategoryListSerializer(serializers.ModelSerializer):

    children = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'name',
            'id',
            'desc', 
            'breadcrumb',
            'children'   
        ]