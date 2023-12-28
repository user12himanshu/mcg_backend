from django.urls import path
from .views import *

urlpatterns = [
    # path('', .as_view()),
    path('models/', CarModelsView.as_view()),
    path('brand/', CarBrandsView.as_view()),
    path('year/', CarYearsView.as_view()),
    path('engineType/', EngineTypeView.as_view()),
    path('get-diagnostic/', DiagnosticView.as_view()),
    path('advertisement/', AdvertisementView.as_view()),
    path('get-diagnostic-videos/', DiagnosticVideosView.as_view()),
]
