from django.urls import path
from .views import *

urlpatterns = [
    path('add', AddItemToCartView.as_view(), name="add-item-to-cart"),
    path('edit', EditCartItemView.as_view()),
    path('delete', DeleteCartItemView.as_view()),
    path('', CartDetailView.as_view())
]