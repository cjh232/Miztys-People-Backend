from django.shortcuts import render
from .serializers import *
from django.db.models import Exists
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from .models import *
from django.db.models import Q


def create_404_response(msg):
    return Response({ "msg": msg, "error": True }, status=status.HTTP_404_NOT_FOUND)




# class SearchProductView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     filter_backends = [SearchFilter]

#     permission_classes = [AllowAny]

#     search_fields = ['$title', 'details', 'brand__name']
#     queryset = Product.objects.filter(is_available=True)


class GetProductOptions(APIView):
    permission_classes = [AllowAny]

    """
    Given the product id and the color, this view should
    return all the sizes vailable in this color.
    """

    def get(self, request, p_id=None, format=None):

        color = request.query_params.get('color')

        try:
            product = Product.objects.get(id=p_id, is_available=True)
        except:
            return create_404_response("Product does not exist or is not available.")

        variants = Variant.objects.filter(product=p_id, quantity__gte=1, color__name=color)

        data = {}

        data["color"] = color
        data["sizes"] = variants.values_list('size__value', flat=True)
        
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailsView(APIView):
    permission_classes = [AllowAny]    

    """
    Given the product id, this view should
    return the details associated with this product.
    This includes a list of available colors which will
    be used thereafter to grab avaialble sizes.
    """

    def get(self, request, p_id=None, format=None):

        try:
            product = Product.objects.get(id=p_id, is_available=True)
        except:
            return create_404_response("Product does not exist or is not available.")

        serializer = ProductSerializer(product)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class VariantFilterView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):

        parse = lambda query: query.split(',') if (query is not None) else None

        brands = parse(request.query_params.get("brand"))
        category = request.query_params.get("category")
        sizes = parse(request.query_params.get("size"))
        colors = parse(request.query_params.get("color"))

        variants = Variant.objects.all()

        if sizes is not None:
            variants = variants.filter(size__in=sizes)

        if colors is not None:
            variants = variants.filter(color__in=colors)

        if brands is not None:
            variants = variants.filter(product__brand__id__in=brands)

        if category is not None:
            variants = variants.filter(
                Q(product__category__id=category)  
                | Q(product__sub_category__id=category)
            )

        if not variants.exists():
            return create_404_response("Filters returned no results.")

        variants = variants.distinct('product')

        serialized = VariantListSerializer(variants, many=True)
        
        
        print(sizes, colors)

        return Response(serialized.data, status=status.HTTP_200_OK)


class BrandList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BrandListSerializer
    queryset = Brand.objects.all()


class SizeList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SizeListSerializer
    queryset = Size.objects.all()

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.filter(parent=None)

        
    