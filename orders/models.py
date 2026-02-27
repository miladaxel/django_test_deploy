from django.db import models
from django.conf import settings


class Order(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'Pending'
        paid = 'paid', 'Paid'
        cancelled = 'canceled', 'Canceled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.pending)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order  id : {self.id} - user_id : {self.user.id} - status : {self.status}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Products', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'OrderItem order_id : {self.order.id} - product_id : {self.product.id} - quantity : {self.quantity}'