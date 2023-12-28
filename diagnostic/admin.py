from django.contrib import admin
from .models import *

admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(CarYear)
admin.site.register(EngineType)
admin.site.register(Diagnostic)
admin.site.register(Advertisement)
admin.site.register(DiagnosticVideos)

# Register your models here.
