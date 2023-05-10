from rest_framework import routers

from mohe_api.accounts import views as accounts
from mohe_api.batch import views as batch
from mohe_api.diagnostics import views as diagnostics
from mohe_api.hardware import views as hardware
from mohe_api.kplex import views as kplex
from mohe_api.measurement import views as measurement
from mohe_api.parameter import views as parameter

router = routers.DefaultRouter()

# accounts
router.register('accounts/user', accounts.UserViewSet, basename='user')
# router.register('facility', facility.FacilityViewSet, basename='facility')

# diagnostics
router.register('diagnostics/category', diagnostics.CategoryViewSet, basename='category')
router.register('diagnostics/biomarker', diagnostics.BioMarkerViewSet, basename='biomarker')

# kplex
router.register('kplex/kplex', kplex.KplexViewSet, basename='kplex')
router.register('kplex/batch', batch.BatchViewSet, basename='batch')
router.register('kplex/parameter', parameter.ParameterViewSet, basename='parameter')

# hardware
router.register('hardware/model', hardware.ModelViewSet, basename='model')
router.register('hardware/device', hardware.DeviceViewSet, basename='device')
router.register('hardware/firmware', hardware.FirmwareViewSet, basename='firmware')

# measurements
router.register('measurement/measurement', measurement.MeasurementViewSet, basename='measurement')
router.register('measurement/field', measurement.MeasurementFieldViewSet, basename='measurementfield')
router.register('measurement/asset', measurement.AssetViewset, basename='asset')

urlpatterns = router.urls
