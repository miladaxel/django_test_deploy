from attr.filters import exclude
from django.db import models
from django.db import transaction

class Products(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name




class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    alt = models.CharField(max_length=150,blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"image for product : {self.product.name} - image_id : {self.id} - alt : {self.alt}"


    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_primary:
                ProductImages.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
            super().save(*args, **kwargs)

