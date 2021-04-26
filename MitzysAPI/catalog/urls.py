from django.urls import path
from .views import *

urlpatterns = [
    path('products', ProductList.as_view()),
    path('products/<str:p_id>/', ProductView.as_view()),
    path('products/available-sizes', GetAvailableSizes.as_view()),
    path('products/search', SearchProduct.as_view()),
    path('orders/checkout', CheckoutView.as_view()),
    path('orders', ListUsersOrders.as_view()),
    path('orders/details/<uuid:order_id>', OrderDetailView.as_view())
]
