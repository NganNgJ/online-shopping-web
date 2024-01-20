from __future__ import absolute_import, unicode_literals
from django.http import JsonResponse, FileResponse,HttpResponse
from rest_framework.response import Response 
from twilio.rest import Client
from celery import shared_task
from .models import (Order, Product, OrderItem, Users)
from  sellweb import settings
from .messages import MESSAGE_TEMPLATE

@shared_task(serializer='json')
def create_order_item(order_items_data, order_id):
    order = Order.objects.get(id=order_id)
    for order_item in order_items_data:
        product_id = order_item['product']
        quantity = order_item['quantity']
        product = Product.objects.get(id=product_id)
        order_item_price = product.price * quantity
        OrderItem.objects.create(order=order, product=product, quantity=quantity, order_item_price=order_item_price)
    
    #get user phone number
    user = Users.objects.get(id=order.buyer_id)
    user_phone_no = str(user.phone)

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body=MESSAGE_TEMPLATE[2001].format(order_id),
            from_=settings.CALL_ID_PHONE,
            to=user_phone_no
                    )
    print(message.sid)
    return Response('Successful created order items')


