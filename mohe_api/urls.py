from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', include('mohe_api.api_urls')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('openapi/', get_schema_view(title='MOHE API', version='0.1', urlconf='mohe_api.api_urls'), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

]
