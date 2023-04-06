from django.urls import path, include
from rest_framework import routers

from mohe_api.accounts import views as accounts
from mohe_api.batch import views as batch
from mohe_api.diagnostics import views as diagnostics
from mohe_api.facility import views as facility
from mohe_api.kplex import views as kplex
from mohe_api.measurement import views as measurement
from mohe_api.parameter import views as parameter

app_name = 'api'

router = routers.DefaultRouter()

# accounts
router.register('user', accounts.UserViewSet, basename='user')
router.register('facility', facility.FacilityViewSet, basename='facility')

# diagnostics
router.register('biomarker', diagnostics.BioMarkerViewSet, basename='biomarker')

# kplex
router.register('kplex', kplex.KplexViewSet, basename='kplex')
router.register('batch', batch.BatchViewSet, basename='batch')
router.register('parameter', parameter.ParameterViewSet, basename='parameter')

# measurements
router.register('measurement/measurement', measurement.MeasurementViewSet, basename='measurement')
router.register('measurement/field', measurement.MeasurementFieldViewSet, basename='measurementfield')
router.register('measurement/asset', measurement.AssetViewset, basename='asset')

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
