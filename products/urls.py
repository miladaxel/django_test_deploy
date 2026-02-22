from django.urls import path

from products.views import ProductListCreateAPIView, ProductDetailAPIView
from products import views

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailAPIView.as_view(), name='category-detail'),
    path( 'products/<int:pk>/images/', views.ProductImageListCreateAPIView.as_view(), name='product-image-list-create'),
    path('product-images/<int:pk>/', views.ProductImageDestroyAPIView.as_view(), name='product-image-destroy'),
]