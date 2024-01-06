from rest_framework import serializers

from notification.models import Notification
from user.serializers import UserSerializer
from shop.serializers import ShopSerializer, CartItemSerializer
from autofind.serializers import ConsultUsSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cart_item = CartItemSerializer(read_only=True)
    slot = ConsultUsSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
