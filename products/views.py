from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Products, Category
from .pagination import StandardResultsSetPagination
from .serializers import ProductsSerializer, CategorySerializer


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Products.objects.filter(status=Products.Status.PUBLISHED).order_by('-published_at', '-created_at')
    serializer_class = ProductsSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = {
        'price': ['gte', 'lte'],
        'stock': ['gte', 'lte'],
        'category': ['exact'],
    }

    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'price', 'stock']
    ordering = ('created_at',)



# class ProductDetailAPIView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Products, pk=pk)
#
#     def get(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductsSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductsSerializer(product, data=request.data)
#         if serializer.is_valid():
#             product = serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductsSerializer(product, data=request.data)
#         if serializer.is_valid():
#             product = serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         product = self.get_object(pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer