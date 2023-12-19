from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from knox.auth import AuthToken
from knox.settings import CONSTANTS
from rest_framework.response import Response

from .serializers import *


class ShopMixinView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    serializer_class = ShopSerializer

    lookup_field = 'pk'

    # authentication_classes = []

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Shop.objects.none()
        return Shop.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        print("working")
        if kwargs.get('pk') is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=user)

    def perform_update(self, serializer):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=user)

    def perform_destroy(self, instance):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")


class ProductMixinView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    serializer_class = ProductSerializer

    lookup_field = 'pk'

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Shop.objects.none()
        return Products.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")


class CartView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        request = self.request
        user = request.user
        qs = CartItem.objects.filter(owner=user).order_by('-date_added')
        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.products.name)
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        product_id = self.request.data.get("products")

        product = Products.objects.filter(id=product_id).first()

        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user, products=product)