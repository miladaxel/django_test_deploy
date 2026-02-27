from django.urls import path
from orders import views

urlpatterns = [
    path('checkout/', views.CheckoutAPIView.as_view(), name='checkout'),
    path('orders/', views.OrderListAPIView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='order-detail'),
]