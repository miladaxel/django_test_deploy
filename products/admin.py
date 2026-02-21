from django.contrib import admin
from products.models import *

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass