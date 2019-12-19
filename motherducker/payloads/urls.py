from django.urls import path
from .views import index, download_payload, any_rest_api


urlpatterns = [
    path('', index, name='index'),
    path('shell', download_payload),
    path('any_rest_api', any_rest_api)
]
