from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import *
from products.models import Variant
from .utils import *
from .serializers import *


# Create your views here.

class AddItemToCartView(APIView):
    permission_classes = [AllowAny]
    item_id_query_lookup = 'item_id'
    quantity_query_lookup = 'quantity'

    def post(self, request, format=None):
        user = request.user

        user_cart = get_or_create_user_cart(user)

        item_id = request.query_params.get(self.item_id_query_lookup)
        quantity = request.query_params.get(self.quantity_query_lookup)

        try:
            variant = Variant.objects.get(id=item_id)
        except ObjectDoesNotExist as error:
            data = {
                "msg": "No item was found under the given id.",
                "error": True,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if variant.num_available < int(quantity):
            data = {
                "msg": "You cannot add this item, with this quantity, to the cart.",
                "error": True,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        try:

            existing_cart_item = CartItem.objects.get(
                variant=variant,
                cart=user_cart
            )

            if variant.num_available < existing_cart_item.quantity + int(quantity):
                data = {
                    "msg": "You cannot add this item, with this quantity, to the cart.",
                    "error": True,
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            existing_cart_item.quantity = existing_cart_item.quantity + int(quantity)
            existing_cart_item.save()

        except ObjectDoesNotExist as error:

            cart_item = CartItem(cart=user_cart, variant=variant, quantity=quantity)
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
        user = request.user

        cart_item_id = data["cart_item_id"]
        new_quantity = data["quantity"]

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except ObjectDoesNotExist as error:
            response_data = {
                "msg": "No cart item was found under given id.",
                "error": True,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        if not user_is_authorized(cart_item.cart.owner, user):
            return Response(
                {
                    "msg": "This account is not authorized to take this action.",
                    "error": True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        cart_item.quantity = new_quantity
        cart_item.save()

        response_data = {
            "msg": "Cart item successfully edited",
            "error": False,
        }

        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class DeleteCartItemView(APIView):
    permission_classes = [AllowAny]
    cart_item_id_lookup_keyword = 'cart_item_id'

    def delete(self, request, format=None):
        user = request.user
        cart_item_id = request.query_params.get(self.cart_item_id_lookup_keyword)

        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except ObjectDoesNotExist as error:

            return Response(
                {
                    "msg": "No cart item was found under the given id.",
                    "error": True
                },
                status=status.HTTP_404_NOT_FOUND)

        if not user_is_authorized(cart_item.cart.owner, user):
            return Response(
                {
                    "msg": "This account is not authorized to take this action.",
                    "error": True
                },
                status=status.HTTP_403_FORBIDDEN
            )

        cart_item.delete()

        response_data = {
            "msg": "Cart item successfully deleted!",
            "error": False
        }

        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class CartDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user = request.user

        user_cart = get_or_create_user_cart(user)

        serializer = CartSerializer(user_cart)

        return Response(serializer.data, status=status.HTTP_200_OK)
