from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.

admin.site.register(ExpertCategory)
admin.site.register(ExpertSubcategory)
admin.site.register(ShopSubscription)
admin.site.register(ShopSubscriptionCharges)

admin.site.register(DiagnosticSubscriptionCharges)
admin.site.register(Enquiry)


class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['phone', 'email']


class CustomDiagnosticSubscriptionAdmin(admin.ModelAdmin):
    search_fields = ['user__phone']
    list_display = ('user',)


admin.site.register(DiagnosticSubscription, CustomDiagnosticSubscriptionAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
