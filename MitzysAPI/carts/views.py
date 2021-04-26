from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError, ObjectDoesNotExist 
from .models import *
from products.models import Item

# Create your views here.

class AddItemToCartView(APIView):
    permission_classes = [AllowAny]
    item_id_query_lookup = 'item_id'
    quantity_query_lookup = 'quantity'

    def get_or_create_user_cart(self, user):

        cart_queryset = Cart.objects.filter(
            owner=user,
            status='O'
        )

        if not cart_queryset.exists():
            new_cart = Cart(owner=user)
            new_cart.save()
            return new_cart
        else:
            return cart_queryset[0]

    def post(self, request, Format=None):
        user = request.user

        user_cart = self.get_or_create_user_cart(user)

        item_id = request.query_params.get(self.item_id_query_lookup)
        quantity = request.query_params.get(self.quantity_query_lookup)        

        try:
            item = Item.objects.get(id=item_id)
        except ObjectDoesNotExist  as error:            
            data = {
                "msg": "No item was found under the given id.",
                "error": True,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if item.num_available < int(quantity):
            data = {
                "msg": "You cannot add this item, with this quantity, to the cart.",
                "error": True,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        try:

            existing_cart_item = CartItem.objects.get(
                item = item, 
                cart = user_cart
            )

            if item.num_available < existing_cart_item.quantity + int(quantity) :
                data = {
                    "msg": "You cannot add this item, with this quantity, to the cart.",
                    "error": True,
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)


            existing_cart_item.quantity = existing_cart_item.quantity + int(quantity)
            existing_cart_item.save()

        except ObjectDoesNotExist  as error:

            cart_item = CartItem(cart=user_cart, item=item, quantity=quantity)
            cart_item.save()


        response_data = {
            "msg": "Item successfully added!",
            "error": False
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class EditCartItemView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, format=None):
        data = request.data
        # user = request.user

        cart_item_id = data["cart_item_id"]
        new_quanity = data["quantity"]

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except ObjectDoesNotExist as error:
            response_data = {
                "msg": "No cart item was found under given id.",
                "error": True,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = new_quanity
        cart_item.save()

        response_data = {
                "msg": "Cart item successfully edited",
                "error": False,
            }

        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
            
        

