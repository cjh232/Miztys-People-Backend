from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from .models import *

# Create your views here.
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category__name', 'sub_category__name', 'brand__name']
    ordering_fields = ['date_added', 'brand__name']

    # Default order
    ordering = ['date_added']


    permission_classes = [AllowAny]
    queryset = Product.objects.filter(is_available=True)


class SearchProduct(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]

    permission_classes = [AllowAny]

    search_fields = ['$title', 'details', 'brand__name']
    queryset = Product.objects.filter(is_available=True)


class GetAvailableSizes(APIView):
    """
    Given product_id and color, returns the sizes available.
    """

    permission_classes = [AllowAny]

    def get_queryset(self):

        return Item.objects.filter(
            product__id = self.request.query_params.get("product_id"),
            num_available__gte=1
        )


    def get(self, request, format=None):

        item_queryset = self.get_queryset()
        product_id = request.query_params.get("product_id")
        color = request.query_params.get("color")

        if not item_queryset.exists():
            return Response({
                "msg": "No item with given product id was found.",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        item_queryset_with_color_match = item_queryset.filter(color=color).distinct("size")

        if not item_queryset_with_color_match.exists():
            return Response({
                "msg": "This product is not available in this color.",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        available_sizes = item_queryset_with_color_match.values_list("size", "id")

        response_data = {
            "product_id": product_id,
            "color": color,
            "available-sizes": available_sizes
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ProductDetailsView(APIView):
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'product_id'

    def get_product_available_colors(self, product_id):
        items = Item.objects.filter(
            product__id=product_id,
            num_available__gte=1
        ).distinct('color')

        return items.values_list('color', flat=True)


    def get(self, request, p_id=None, format=None):

        try:
            product_queryset = Product.objects.filter(id=p_id, is_available=True)
        except ValidationError as error:
              return Response({
                  "msg": "Given product id is formatted incorrectly.",
                  "error": True
              }, status=status.HTTP_400_BAD_REQUEST)

        if not product_queryset.exists():
            return Response({
                "msg": "No product with given id was found.",
                "error": True
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product_queryset[0])

        available_colors = self.get_product_available_colors(p_id)

        data = {}

        data.update(serializer.data)

        data["available_colors"] = available_colors

        return Response(data, status=status.HTTP_200_OK)