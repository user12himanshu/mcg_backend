import datetime

from django.shortcuts import render
from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
import mcg.payment_helper as payment
import base64
from notification.views import createNotificationFromSlot
from cashfree_pg.api_client import Cashfree
from django.conf import settings
from .helpers import is_inside
from django.db.models import Q


class AutoFindView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = AutoFindSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request = self.request
        data = request.query_params
        lat = data.get('lat')
        long = data.get('long')
        if lat and long:
            lat = float(lat)
            long = float(long)
            qs = CustomUser.objects.filter(is_vendor=True, expert_category=data.get('expert_category'))
            qs_final = []
            for q in qs:
                if is_inside(lat, long, q.latitude, q.longitude):
                    qs_final.append(q.id)
            queryset = CustomUser.objects.filter(Q(pk__in=qs_final))
            return queryset
        else:
            return CustomUser.objects.filter(is_vendor=True, pin_code=data.get('pin_code')) | CustomUser.objects.filter(
                is_vendor=True, city=data.get('city'), state=data.get('state'),
                expert_category=data.get('expert_category'))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ConsultUsView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = ConsultUsSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        request = self.request
        data = request.data
        selected_date = data.get('date')
        return Slot.objects.filter(date=selected_date)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        if id:
            return self.update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def perform_update(self, serializer):
        request = self.request
        # data = serializer.data
        instance = serializer.save(booked_by=request.user)
        createNotificationFromSlot(user=request.user, slotId=instance.id)
        # user = request.user
        # instance = self.get_object()
        # instance.booked_by = user
        # instance.booked = True
        # instance.type = data.get('type')
        # instance.save()


class ConsultViewBooked(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ConsultUsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Slot.objects.filter(booked=True)
        else:
            return Slot.objects.filter(booked=True, booked_by=user)

    def get(self, request, *args, **kwargs):
        print(self.queryset)
        return self.list(request, *args, **kwargs)


class ConsultUsAvailableSlotsView(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin,
                                  generics.GenericAPIView):
    serializer_class = ConsultUsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Slot.objects.filter(date__gte=datetime.datetime.now())

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChargesView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ChargesSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Charges.objects.filter(id=1)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PaymentsView(APIView):
    serializer_class = InitPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = InitPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            data.pop('booked')
            data.pop('booked_by')
            data['id'] = str(data['id'])
            data['user_id'] = str(request.user.id)
            if request.data.get("product") == 'NC':
                product_price = Charges.objects.all().first().nc
            else:
                product_price = Charges.objects.all().first().vc
            payment_intent = payment.init_payment(product_price, request.user,
                                                  data)
            return Response(payment_intent)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentsCallBackView(APIView):
    # serializer_class = PaymentCallbackSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data.get('data')
        tags = data['order']['order_tags']
        slot = Slot.objects.get(id=tags['id'])
        if slot:
            user = CustomUser.objects.get(id=tags['user_id'])
            if user:
                slot.booked_by = user
                slot.booked = True
                slot.type = tags['type']
                slot.brand = tags['brand']
                slot.address = tags['address']
                slot.car_model = tags['car_model']
                slot.full_name = tags['full_name']
                slot.voice_call_number = tags['voice_call_number']
                slot.save()
                createNotificationFromSlot(user=user, slotId=slot.id)

        # data = base64.b64decode(request.data['response'])
        # serializer = InitPaymentSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     if request.data.get("product") == 'NC':
        #         product_price = Charges.objects.all().first().nc
        #     else:
        #         product_price = Charges.objects.all().first().vc
        #     payment_intent = payment.init_payment(product_price, request.data.get("product"),
        #                                           request.data.get("owner"),
        #                                           request.data.get("phone"))
        #     return Response(payment_intent)
        return Response({'test': 'test'})
