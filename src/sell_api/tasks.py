from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .models import (Order)

@shared_task
def add(x, y):
    # order = Order.objects.filter(id=1)
    # #...
    # order.save()
    # Notification.Objects.create(user=order.user, is_read=False,...)
    # call api push_notification
    return x + y

