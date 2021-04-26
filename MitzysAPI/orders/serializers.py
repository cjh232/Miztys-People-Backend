from rest_framework import serializers
from products.serializers import ItemsSerializer
from .models import *


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