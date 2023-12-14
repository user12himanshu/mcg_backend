from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopMixinView.as_view()),
    path('<int:pk>/', ShopMixinView.as_view()),
]
