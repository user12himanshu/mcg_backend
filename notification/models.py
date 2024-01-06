from django.db import models
from user.models import CustomUser
from shop.models import CartItem
from autofind.models import Slot


# Create your models here.
class Notification(models.Model):
    type_choices = ((1, 'Bookings'), (2, 'Order'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=type_choices)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, blank=True, null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, blank=True, null=True)
