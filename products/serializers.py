from rest_framework import serializers
from .models import Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'price', 'description',
            'stock', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']