from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth import authenticate
from .models import *
from django.db.models import Count
from .serializers import *
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter 


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

    def get(self, request, format=None):
        data = request.data

        color = data["color"]
        product_id = data["product_id"]

        try:
            item_queryset = Item.objects.filter(product_id=product_id)
        except ValidationError as error:
            return Response({
                  "msg": "Given product_id was formatted incorrectly.",
                  "error": True
              }, status=status.HTTP_400_BAD_REQUEST)

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

        available_sizes = item_queryset_with_color_match.values_list("size", flat=True)

        response_data = {
            "product_id": product_id,
            "color": color,
            "available-sizes": available_sizes
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ProductView(APIView):
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'product_id'

    def get_product_available_colors(self, product_id):
        items = Item.objects.filter(product_id=product_id).distinct('color')

        res = items.values_list('color', flat=True)
        return res

    def get(self, request, p_id=None, format=None):

        try:
            product_queryset = Product.objects.filter(product_id=p_id, is_available=True)
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
