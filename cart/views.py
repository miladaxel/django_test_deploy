from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Products

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartItemCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)

    def post(self, request):
        cart = get_or_create_cart(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)
        product = get_object_or_404(Products, pk=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)

        qty = request.data.get('quantity')
        if qty is None:
            return Response({'quantity': 'this field is required'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            qty = int(qty)
        except ValueError:
            return Response({'quantity': 'quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)
        if qty < 1:
            return Response({'quantity': 'quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = qty
        item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)