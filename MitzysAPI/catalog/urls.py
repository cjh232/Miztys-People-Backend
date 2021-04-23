from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view()),
    path('<str:p_id>/', ProductView.as_view()),
    path('available-sizes', GetAvailableSizes.as_view()),
    path('search', SearchProduct.as_view()),
    path('orders/create', CreateOrderView.as_view())
]
