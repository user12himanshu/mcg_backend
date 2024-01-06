from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import privacy_policy, terms_of_service

urlpatterns = [
    path('privacy-policy/', privacy_policy),
    path('terms-conditions/', terms_of_service),
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),
    path('shop/', include('shop.urls')),
    path('autofind/', include('autofind.urls')),
    path('notification/', include('notification.urls')),
    path('diagnostic/', include('diagnostic.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
