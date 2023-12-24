from django.db import models
from user.models import CustomUser
from mcg.utility import phone_regex


# Create your models here.
class Slot(models.Model):
    call_choices = (('NC', 'Voice Call'), ('VC', 'Video Call'))
    type = models.CharField(
        max_length=2,
        choices=call_choices,
        blank=True,
        null=True
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=120, blank=True, null=True)
    brand = models.CharField(max_length=120, blank=True, null=True)
    car_model = models.CharField(max_length=120, blank=True, null=True)
    address = models.CharField(max_length=120, blank=True, null=True)
    voice_call_number = models.CharField(max_length=120, blank=True, null=True, validators=[phone_regex])
    car_problems = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.date.__str__() + " " + self.start_time.__str__()


class Charges(models.Model):
    vc = models.IntegerField()
    nc = models.IntegerField()
