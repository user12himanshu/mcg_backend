from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *
from .permissions import IsOwnerPermission
from autofind.serializers import AutoFindSerializer
from knox import views as knox_views
from django.contrib.auth import login
from rest_framework import generics
from .models import ShopSubscription
import datetime
from dateutil.relativedelta import relativedelta
import mcg.payment_helper as payment


class CreateUserAPI(CreateAPIView, generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    # def get_permissions(self):
    #     return [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response.data, status=status.HTTP_200_OK)


class ExpertCategoryMixin(ListModelMixin, GenericAPIView):
    serializer_class = ExpertCategorySerializer
    permission_classes = [AllowAny]
    queryset = ExpertCategory.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetAllSellers(ListModelMixin, generics.GenericAPIView):
    serializer_class = AutoFindSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.filter(is_vendor=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CheckShopSubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        obj = ShopSubscription.objects.filter(user=user)
        if obj.exists():
            if obj.first().valid_till > datetime.date.today():
                return Response({'subscribed': True})
            return Response({'subscribed': False})
        return Response({'subscribed': False})


class ShopSubscriptionChargesView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = ShopSubscriptionCharges.objects.get(id=1)
        serializer = ShopSubscriptionChargesSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddShopSubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSubsriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        obj = ShopSubscription.objects.filter(user=user)
        type = request.data.get("type")
        if not type:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        valid_till = datetime.date.today()
        to_update = False
        if obj.exists():
            to_update = True
            sub = obj.first()
            if sub.valid_till >= datetime.date.today():
                valid_till = sub.valid_till

        if type == "MONTHLY":
            valid_till = valid_till + relativedelta(months=1)
        elif type == "QUARTERLY":
            valid_till = valid_till + relativedelta(months=3)
        elif type == "HALFYEARLY":
            valid_till = valid_till + relativedelta(months=6)
        elif type == "YEARLY":
            valid_till = valid_till + relativedelta(months=12)

        serializer = self.get_serializer()

        if to_update:
            sub = obj.first()
            sub.valid_till = valid_till
            sub.save()
            serializer = ShopSubsriptionSerializer(sub)
        else:
            obj = ShopSubscription.objects.create(user=user, date_added=datetime.datetime.now(),
                                                  valid_till=valid_till, type=type)
            obj.save()
            serializer = ShopSubsriptionSerializer(obj)

        return Response(serializer.data)


class InitShopSubscriptionPayment(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        type = request.data.get("type")
        user = request.user
        obj = ShopSubscriptionCharges.objects.get(id=1)
        if type == "MONTHLY":
            price = obj.monthly
        elif type == "QUARTERLY":
            price = obj.quarterly
        elif type == "HALFYEARLY":
            price = obj.half_yearly
        elif type == "YEARLY":
            price = obj.yearly
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        payment_intent = payment.init_payment(float(price), user.id, user.phone)
        return Response(payment_intent)


class CheckDiagnosticSubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        obj = DiagnosticSubscription.objects.filter(user=user)
        if obj.exists():
            if obj.first().valid_till > datetime.date.today():
                return Response({'subscribed': True})
            return Response({'subscribed': False})
        return Response({'subscribed': False})


class DiagnosticSubscriptionChargesView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = DiagnosticSubscriptionCharges.objects.get(id=1)
        serializer = DiagnosticSubscriptionChargesSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddDiagnosticSubscriptionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiagnosticSubsriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        obj = DiagnosticSubscription.objects.filter(user=user)
        type = request.data.get("type")
        if not type:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        valid_till = datetime.date.today()
        to_update = False
        if obj.exists():
            to_update = True
            sub = obj.first()
            if sub.valid_till >= datetime.date.today():
                valid_till = sub.valid_till

        if type == "MONTHLY":
            valid_till = valid_till + relativedelta(months=1)
        elif type == "QUARTERLY":
            valid_till = valid_till + relativedelta(months=3)
        elif type == "HALFYEARLY":
            valid_till = valid_till + relativedelta(months=6)
        elif type == "YEARLY":
            valid_till = valid_till + relativedelta(months=12)

        serializer = self.get_serializer()

        if to_update:
            sub = obj.first()
            sub.valid_till = valid_till
            sub.save()
            serializer = DiagnosticSubsriptionSerializer(sub)
        else:
            obj = DiagnosticSubscription.objects.create(user=user, date_added=datetime.datetime.now(),
                                                        valid_till=valid_till, type=type)
            obj.save()
            serializer = DiagnosticSubsriptionSerializer(obj)

        return Response(serializer.data)


class InitDiagnosticSubscriptionPayment(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        type = request.data.get("type")
        user = request.user
        obj = DiagnosticSubscriptionCharges.objects.get(id=1)
        if type == "MONTHLY":
            price = obj.monthly
        elif type == "QUARTERLY":
            price = obj.quarterly
        elif type == "HALFYEARLY":
            price = obj.half_yearly
        elif type == "YEARLY":
            price = obj.yearly
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        payment_intent = payment.init_payment(float(price), user.id, user.phone)
        return Response(payment_intent)
