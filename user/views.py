from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *
from .permissions import IsOwnerPermission
from knox import views as knox_views
from django.contrib.auth import login


class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return CustomUser.objects.none()
        return qs.filter(phone=user.phone)


class CreateVendorUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateVendorUserSerializer
    permission_classes = [AllowAny]


class UpdateVendorUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateVendorUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user

        if not user.is_authenticated:
            return CustomUser.objects.none()
        return qs.filter(id=user.id)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data, status=status.HTTP_200_OK)
