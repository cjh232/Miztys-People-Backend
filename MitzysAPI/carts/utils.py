from .models import *


def get_or_create_user_cart(user):
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


def user_is_authorized(user1, user2):
    return user1 == user2
