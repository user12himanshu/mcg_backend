from django.urls import path
from .views import *
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view()),
    path('create-expertuser/', CreateVendorUserAPI.as_view()),
    path('update-expertuser/<int:pk>/', UpdateVendorUserAPI.as_view()),
    path('login/',  LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('experts/', ExpertCategoryMixin.as_view()),
]