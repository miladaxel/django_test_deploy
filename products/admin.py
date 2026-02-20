from django.contrib import admin
from products.models import *

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    pass
