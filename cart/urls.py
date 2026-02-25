from django.urls import path
from cart import views


urlpatterns = [
    path('cart/', views.CartAPIView.as_view(), name='cart'),
    path('cart/items/', views.CartItemCreateView.as_view(), name='cart_item-create'),
    path('cart/items/<int:pk>/', views.CartItemDetailView.as_view(), name='cart_item-detail'),
]