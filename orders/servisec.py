from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from products.models import Products
from .models import Order, OrderItem


class CheckoutError(Exception):
    pass



#با استفاده از transaction.atomic یک فانکشن برای حذف سبد خرید و تبدیل به order و همچنین اپذت مقادیر دیتابیس تعریف می کنیم
#این فانکشن یه یوزر میگیره و یه ابجکت از نوع order  تحویل میده
@transaction.atomic
def checkout_cart(user) -> Order:
    cart = get_object_or_404(Cart, user=user)

    #ایتم های داخل کارت رو می گیریم و تو یه لیست ذخیره می کنیم برای جلوگیری از چند بار کویری زدن چون چند جا نیازشون داریم
    cart_items = list(CartItem.objects.filter(cart=cart).select_related('product'))
    if not cart_items:
        raise CheckoutError('Cart is empty')

    #ایدی هر محصول راخل cart items  رو میگیریم و داخل یه لیست ذخیره می کنیم
    product_ids = [ci.product.id for ci in cart_items]
    #برای جلوگیری از rase condition از select for update استفاده میکنیم که ایتم هارو تا پایان عملیات قفل کنیم
    #از id__in استفاده کردیم که فقط محصولاتی که ایدیشون تو سبد خرید هست رو قفل کنیم , این باعث کمترین کویری میشه
    #از in bulk  استفاده میکنیم که باعث میشه یه دیکشنری با کلید id برگردونه و این باعث میشه کویریمون مرتبش o(n) باشه
    locked_products = (Products.objects.select_for_update().filter(id__in=product_ids).in_bulk(field_name='id'))

    for ci in cart_items:
        p = locked_products.get(ci.product.id)
        if p is None :
            raise CheckoutError(f'Product with id {ci.product.id} not found')
        if p.status != Products.Status.PUBLISHED :
            raise CheckoutError(f'Product with id {ci.product.id} has not available')
        if p.stock < ci.quantity :
            raise CheckoutError(f'not enough stock for product with id {ci.product.id}')

    order = Order.objects.create(user=user, status=Order.Status.pending)

    total = 0
    item_to_create = []
    for ci in cart_items:
        p = locked_products[ci.product.id]
        unit_price = p.price
        line_total = unit_price * ci.quantity
        total += line_total

        item_to_create.append(OrderItem(order=order, product=p, quantity=ci.quantity, unit_price=unit_price, line_total=line_total))

    #  با استفاده از bulk create اطلاعاتی که بالا گرفتیمو ذخیره میکنیم این باعث میشه هر بار .save() نزنیم و کل عملیات یک باره انجام بشه
    OrderItem.objects.bulk_create(item_to_create)
    order.total_price = total
    order.save(update_fields=['total_price'])

    for ci in cart_items:
        #F باعث میشه که عملیات کم کردن میزان محصول مستقیما از توی دیتابیس انجام بشه و از توی فایل پایتونی انجام نشه
        Products.objects.filter(id=ci.product.id).update(stock=F('stock') - ci.quantity)
        CartItem.objects.filter(cart=cart).delete()

    return order