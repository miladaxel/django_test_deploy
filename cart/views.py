from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.db.models import Prefetch

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartItemUpdateSerializer
from products.models import Products

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def get_or_create_cart_with_items(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return (
        Cart.objects
        .filter(pk=cart.pk)
        .prefetch_related(
            Prefetch("items", queryset=CartItem.objects.select_related("product"))
        )
        .get()
    )

class CartAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        cart = get_or_create_cart_with_items(request.user)
        return Response(CartSerializer(cart).data)


class CartItemCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer


    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related('product')
        serialized_items = CartItemSerializer(items, many=True)
        return Response({'items': serialized_items.data})

    def post(self, request):
        cart = get_or_create_cart(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)
        product = get_object_or_404(Products, pk=product_id, status=Products.Status.PUBLISHED)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemUpdateSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def patch(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)

        serializer = self.get_serializer(item, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        cart = get_or_create_cart(request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)