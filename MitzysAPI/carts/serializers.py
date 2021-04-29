from rest_framework import serializers
from .models import *
from products import views


class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='item.product.title')
    product_id = serializers.ReadOnlyField(source='item.product.id')
    color = serializers.ReadOnlyField(source='item.color')
    size = serializers.ReadOnlyField(source='item.size')

    class Meta:
        model = CartItem
        fields = [
            'title',
            'product_id',
            'color',
            'size',
            'quantity'
        ]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Cart
        fields = [
            'id',
            'owner',
            'owner_email',
            'status',
            'cart_items',
            'created_at'
        ]
