from django.urls import path
from .views import index, download_payload


urlpatterns = [
    path('', index, name='index'),
    path('shell', download_payload),
]
