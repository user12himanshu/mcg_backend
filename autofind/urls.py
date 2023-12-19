from django.urls import path
from .views import *

urlpatterns = [
    path('', AutoFindView.as_view()),
    path('consult-us/', ConsultUsView.as_view()),
    path('consult-us/<int:pk>/', ConsultUsView.as_view()),
    path('consult-us/available/', ConsultUsAvailableSlotsView.as_view()),
    path('charges/', ChargesView.as_view()),
    path('pay/', PaymentsView.as_view()),
    path('payment-callback/', PaymentsCallBackView.as_view()),
]
