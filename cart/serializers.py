from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Products

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_id = serializers.IntegerField(write_only=True)

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_id', 'subtotal']

    def get_product(self, obj):
        return {
            'id': obj.product_id,
            'name': obj.product.name,
            'price':str(obj.product.price),
        }

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity

class CartItemUpdateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    class Meta:
        model = CartItem
        fields = ['quantity']




class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_quantity', 'created_at', 'updated_at']

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        total = sum((item.product.price * item.quantity for item in obj.items.all()))
        return str(total)