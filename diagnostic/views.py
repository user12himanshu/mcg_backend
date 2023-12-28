from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *


# Create your views here.

class CarBrandsView(generics.ListAPIView, GenericAPIView):
    serializer_class = CarBrandSerializer
    permission_classes = [IsAuthenticated]

    queryset = CarBrand.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CarModelsView(generics.ListAPIView, GenericAPIView):
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated]

    queryset = CarModel.objects.all()

    def get_queryset(self):
        request = self.request
        brand = CarBrand.objects.get(id=request.query_params.get('brand'))
        queryset = CarModel.objects.filter(brand=brand)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CarYearsView(generics.ListAPIView, GenericAPIView):
    serializer_class = CarYearSerializer
    permission_classes = [IsAuthenticated]

    queryset = CarYear.objects.all()

    def get_queryset(self):
        request = self.request
        model = CarModel.objects.get(id=request.query_params.get('model'))
        queryset = CarYear.objects.filter(car=model)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EngineTypeView(generics.ListAPIView, GenericAPIView):
    serializer_class = EngineTypeSerializer
    permission_classes = [IsAuthenticated]

    queryset = EngineType.objects.all()

    def get_queryset(self):
        request = self.request
        year = CarYear.objects.get(id=request.query_params.get('year'))
        queryset = EngineType.objects.filter(year=year)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DiagnosticView(generics.ListAPIView, GenericAPIView):
    serializer_class = DiagnosticSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        brand = request.query_params.get('brand')
        model = request.query_params.get('model')
        year = request.query_params.get('year')
        engineType = request.query_params.get('engine_type')

        car_brand = CarBrand.objects.get(id=brand)
        car_model = CarModel.objects.get(id=model)
        car_year = CarYear.objects.get(id=year)
        car_engine_type = EngineType.objects.get(id=engineType)

        queryset = Diagnostic.objects.filter(brand=car_brand, car=car_model, year=car_year, engine_type=car_engine_type)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DiagnosticVideosView(generics.ListAPIView, GenericAPIView):
    serializer_class = DiagnosticVideosSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        brand = request.query_params.get('brand')
        model = request.query_params.get('model')

        car_brand = CarBrand.objects.get(id=brand)
        car_model = CarModel.objects.get(id=model)

        queryset = DiagnosticVideos.objects.filter(brand=car_brand, car=car_model)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AdvertisementView(generics.ListAPIView, GenericAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated]
    queryset = Advertisement.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
