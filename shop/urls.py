from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopMixinView.as_view()),
    path('<int:pk>/', ShopMixinView.as_view()),
    path('products/<int:owner>/', ProductMixinView.as_view()),
    path('products/', ProductMixinView.as_view()),
    path('cart/', CartView.as_view()),
    path('cart/<int:pk>/', CartView.as_view()),
    path('upload-shop-image/', ShopImagesView.as_view()),
    path('order-all/', OrderViewSet.as_view()),
    path('add-description/', DescriptionView.as_view()),
    path('add-about/', AboutView.as_view()),
    path('upload-product-images/', ProductImagesView.as_view()),
]
