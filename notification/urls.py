from django.urls import path, include

from notification.views import NotificationView

urlpatterns = [
    path('', NotificationView.as_view(), name='notification')
]