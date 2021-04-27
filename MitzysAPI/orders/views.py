from django.shortcuts import render

# Create your views here.

# class CheckoutView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, format=None):
#         data = request.data
#         user = request.user
#
#         # User's cart must be `ongoing` to avoid editing previous carts
#         user_cart = Cart.objects.get(owner=user, status='O')
#         user_order = Order(owner=user)
#         cart_items = CartItem.objects.filter(cart=user_cart)
#
#         invalid_cart_items = get_invalid_cart_items(cart_items)
#
#         if len(invalid_cart_items) > 0:
#             data = {
#                 "msg": "Some items in the cart are not available.",
#                 "invalid_cart_items": invalid_cart_items,
#                 "error": True
#             }
#             return Response(
#                 data, status=status.HTTP_409_CONFLICT
#             )
#         else:
#             user_order.save()
#             create_order_items(cart_items, user_order)
#
#             # Change user cart status to finished.
#             user_cart.status = 'F'
#             user_cart.save()
#             return Response(status=status.HTTP_200_OK)
#
#
#
#             )

# class ListUsersOrders(generics.ListAPIView):
#     serializer_class = OrderSerializer
#
#     def get_queryset(self):
#         """
#         This view should return a list of all the orders
#         for the currently authenticated user.
#         """
#
#         user = self.request.user
#         return Order.objects.filter(owner=user)
#
#
# class OrderDetailView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request, order_id, format=None):
#         order_items_queryset = OrderItem.objects.filter(order__id=order_id)
#
#         if order_items_queryset.exists():
#             serializer = OrderItemSerializer(order_items_queryset, many=True)
#
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {
#                     "msg": "Order details could not be found the the given order id.",
#                     "error": True
#                 },
#                 status=status.HTTP_404_NOT_FOUND