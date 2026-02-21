from django.utils import timezone

from rest_framework import serializers
from unicodedata import category

from .models import Products, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class ProductsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category' ,queryset=Category.objects.all(), write_only=True,
        required=False, allow_null=True
                  )
    class Meta:
        model = Products
        fields = [
            'id', 'name', 'price', 'description',
            'stock', 'created_at', 'category', 'category_id',
            'status', 'published_at'
        ]
        read_only_fields = ['id', 'created_at', 'published_at']


    def validate(self, attrs):
        instance = getattr(self, 'instance', None)

        new_status = attrs.get('status', instance.status if instance else Products.Status.DRAFT)
        if new_status == Products.Status.PUBLISHED:
            category = attrs.get('category', instance.category if instance else None)
            price = attrs.get('price', instance.price if instance else None)
            stock = attrs.get('stock', instance.stock if instance else None)

            errors = {}
            if category is None:
                errors['category'] = 'Category required to publish a product'
            if price is None or price <= 0:
                errors['price'] = 'Price must be a positive number'
            if stock is None or stock <= 0:
                errors['stock'] = 'Stock must be a positive number'

            if errors:
                raise serializers.ValidationError(errors)
        return attrs

    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        obj = super().update(instance, validated_data)

        if old_status != Products.Status.PUBLISHED and new_status == Products.Status.PUBLISHED:
            if obj.published_at is None:
                obj.published_at = timezone.now()

                obj.save(update_fields=['published_at'])

        return obj

