from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse, FileResponse,HttpResponse
from rest_framework.response import Response 

from celery import shared_task

from .models import (Order,Product,OrderItem)

@shared_task(serializer='json')
def create_order_item(order_items_data, order_id):
    order = Order.objects.get(id=order_id)
    for order_item in order_items_data:
        product_id = order_item['product']
        quantity = order_item['quantity']
        product = Product.objects.get(id=product_id)
        order_item_price = product.price * quantity
        OrderItem.objects.create(order=order, product=product, quantity=quantity, order_item_price=order_item_price)
    return Response('Successful created order items')


