from django.db import models


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

    def __str__(self):
        return self.date.__str__() + " " + self.start_time.__str__()


class Charges(models.Model):
    vc = models.IntegerField()
    nc = models.IntegerField()
