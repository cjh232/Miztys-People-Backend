from django.urls import path
from .views import *

urlpatterns = [
    path('details/<str:p_id>/', ProductDetailsView.as_view()),
    path('details/<str:p_id>/options/', GetProductOptions.as_view()),
    path('list/', VariantFilterView.as_view()),
    path('brands/', BrandList.as_view()),
    path('sizes/', SizeList.as_view()),
    path('categories/', CategoryListView.as_view()),
]