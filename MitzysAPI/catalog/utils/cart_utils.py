from catalog.models import *


def make_item_unavailable(item):
        item.is_available = False
        item.save()


def get_invalid_cart_items(cart_items):

        seen_items = []
        unavailable_items = []

        for cart_item in cart_items:
            item_queryset = Item.objects.filter(
                product = cart_item.product,
                size = cart_item.size,
                color = cart_item.color,
                is_available=True
            ).exclude(
                id__in=seen_items
            )

            if not item_queryset.exists():
                unavailable_items.append(cart_item.id)
        
        return unavailable_items

def create_order_items(cart_items, order):

        print('creating order items...')
        order_items = []

        
        for cart_item in cart_items:
            item_queryset = Item.objects.filter(
                product = cart_item.product,
                size = cart_item.size,
                color = cart_item.color,
                is_available=True
            )

            item = item_queryset[0]
            make_item_unavailable(item)

            order_item = OrderItem(order = order, item = item)
            order_items.append(order_item)
            order_item.save()
        
        return order_items