from rest_framework import mixins, generics
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
