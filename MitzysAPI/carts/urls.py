from django.urls import path
from .views import *

urlpatterns = [
    path('add', AddItemToCartView.as_view()),
    path('edit', EditCartItemView.as_view())
]