from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView

from .models import Products
from .serializers import ProductsSerializer

# class ProductListCreateAPIView(APIView):
#     def get(self, request):
#         qs = Products.objects.all().order_by('created_at')
#         serializer = ProductsSerializer(qs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = ProductsSerializer(data=request.data)
#         if serializer.is_valid():
#             product = serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer



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