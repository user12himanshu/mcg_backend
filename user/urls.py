from django.urls import path
from .views import *
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view()),
    path('create-expertuser/', CreateVendorUserAPI.as_view()),
    path('update-expertuser/<int:pk>/', UpdateVendorUserAPI.as_view()),
    path('all-sellers/', GetAllSellers.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('experts/', ExpertCategoryMixin.as_view()),
    path('check-shop-subscription/', CheckShopSubscriptionView.as_view()),
    path('add-shop-subscription/', AddShopSubscriptionView.as_view()),
    path('shop-subscription-charges/', ShopSubscriptionChargesView.as_view()),
    path('init-shop-subscription/', InitShopSubscriptionPayment.as_view()),
    path('check-diagnostic-subscription/', CheckDiagnosticSubscriptionView.as_view()),
    path('add-diagnostic-subscription/', AddDiagnosticSubscriptionView.as_view()),
    path('diagnostic-subscription-charges/', DiagnosticSubscriptionChargesView.as_view()),
    path('init-diagnostic-subscription/', InitDiagnosticSubscriptionPayment.as_view()),
]
