import datetime

from rest_framework import mixins, generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from knox.auth import AuthToken
from knox.settings import CONSTANTS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save(owner=user)
            for imageId in request.data.get('shop_images'):
                image = ShopImages.objects.filter(id=imageId).first()
                instance.shop_images.add(image)
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


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


class ShopImagesView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ShopImagesSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    queryset = ShopImages.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductImagesView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = ProductImagesSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    queryset = ProductImages.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DescriptionView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = DescriptionSerializer
    permission_classes = [IsAuthenticated]

    queryset = Description.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AboutView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = AboutSerializer
    permission_classes = [IsAuthenticated]

    queryset = Description.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductMixinView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    serializer_class = ProductSerializer

    lookup_field = 'pk'

    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Shop.objects.none()
        return Products.objects.filter(owner__owner__shopsubscription__valid_till__gt=datetime.date.today())

    def get(self, request, *args, **kwargs):
        if kwargs.get('owner'):
            owner = self.request.user
            shop = Shop.objects.filter(id=self.kwargs['owner']).first()
            qs = Products.objects.filter(owner=shop)
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data)
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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            raise ValueError("You are not allowed to perform this action.")
        if not user.is_vendor:
            raise ValueError("You are not allowed to perform this action.")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            shop = Shop.objects.get(id=self.request.data['shopId'])
            instance = serializer.save(owner=shop)
            for imageId in request.data.get('product_images'):
                image = ProductImages.objects.filter(id=imageId).first()
                instance.product_images.add(image)
            for descriptionId in request.data.get('description'):
                description = Description.objects.filter(id=descriptionId).first()
                instance.description.add(description)
            for aboutId in request.data.get('about'):
                about = About.objects.filter(id=aboutId).first()
                instance.about.add(about)
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        return self.destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        product_id = self.request.data.get("products")

        product = Products.objects.filter(id=product_id).first()

        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=self.request.user, products=product)


class OrderViewSet(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(products__owner__owner=user).order_by('-date_added')
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
