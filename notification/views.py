from django.shortcuts import render
from rest_framework import generics, permissions

from autofind.models import Slot
from shop.models import CartItem
from .serializers import NotificationSerializer
from .models import Notification


# Create your views here.
class NotificationView(generics.CreateAPIView, generics.ListAPIView, generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        request = self.request
        return Notification.objects.filter(user=request.user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def createNotificationFromSlot(user, slotId):
    slot = Slot.objects.get(id=slotId)
    return Notification.objects.create(type=1, slot=slot, user=user)


def createNotificationFromCartItem(user, cartItemId):
    cartItem = CartItem.objects.get(id=cartItemId)
    return Notification.objects.create(type=2, cart_item=cartItem, user=user)
