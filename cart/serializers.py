from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Products

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_id']

    def get_product(self, obj):
        return {
            'id': obj.product_id,
            'name': obj.product.name,
            'price':str(obj.product.price),
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']