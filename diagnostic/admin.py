from django.contrib import admin
from .models import *

admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(CarYear)
admin.site.register(Diagnostic)

# Register your models here.
