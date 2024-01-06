import json

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
from rest_framework.decorators import api_view
from .models import ShopSubscription
import datetime
import requests
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


class UpdateExpertUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateExpertUserSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        user = request.user
        if not user.is_authenticated:
            return CustomUser.objects.none()
        return qs.filter(phone=user.phone)


class UpdateUserPasswordAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     phone = self.request.query_params.get('phone')
    #     return qs.filter(phone=phone)


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


class SendOtpView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        forgot_pass = request.data.get("forgot_pass")
        print('here')
        if forgot_pass:
            url = f"http://www.smsalert.co.in/api/mverify.json?apikey=65906255a7355&sender=MCGAUT&mobileno={phone}&template=Remembering the password can be a headache. You can reset your password for MCG AutoFind by entering this OTP - [otp]"
        else:
            url = f"http://www.smsalert.co.in/api/mverify.json?apikey=65906255a7355&sender=MCGAUT&mobileno={phone}&template=You are just one step away from registering to MCG AutoFind. Here is your OTP for signing up - [otp]"
        res = requests.post(url)
        if res.status_code == 200:
            return Response({'sent': 'success'}, status.HTTP_200_OK)
        return Response({'sent': 'failed'}, status.HTTP_403_FORBIDDEN)


class ValidateOtpView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        code = request.data.get('code')

        url = f"http://www.smsalert.co.in/api/mverify.json?apikey=65906255a7355&mobileno={phone}&code={code}"
        res = requests.post(url)
        data = json.loads(res.text)
        if res.status_code == 200:
            if data['description']['desc'] == "Code Matched successfully.":
                return Response({'verify': 'success'}, status.HTTP_200_OK)

        return Response({'sent': 'failed', 'message': data['description']["desc"]}, status.HTTP_400_BAD_REQUEST)


class CheckUserExistsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def getQueryset(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        qs = CustomUser.objects.filter(phone=phone)
        return qs

    def get(self, request, *args, **kwargs):
        if self.getQueryset(request).exists():
            return Response({'exist': True}, status.HTTP_200_OK)
        else:
            return Response({'exist': False}, status.HTTP_200_OK)


class GetUserIdView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def getQueryset(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        qs = CustomUser.objects.filter(phone=phone)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.getQueryset(request)
        if qs.exists():
            return Response({'id': qs.first().id}, status.HTTP_200_OK)
        else:
            return Response({'exist': False}, status.HTTP_400_BAD_REQUEST)


class GetUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ExpertSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class EnquiryView(CreateAPIView, generics.GenericAPIView):
    permissions = [IsAuthenticated]
    serializer_class = EnquirySerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
