from django.urls import path
from .views import download_payload, any_rest_api, backdoor_api


urlpatterns = [
    path('shell', download_payload),
    path('any_rest_api', any_rest_api),
    path('backdoor_api/<slug:uuid>', backdoor_api)
]