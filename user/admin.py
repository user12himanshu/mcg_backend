from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(ExpertCategory)
admin.site.register(ExpertSubcategory)
admin.site.register(ShopSubscription)
admin.site.register(ShopSubscriptionCharges)
admin.site.register(DiagnosticSubscription)
admin.site.register(DiagnosticSubscriptionCharges)

