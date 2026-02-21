from django.db import models

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