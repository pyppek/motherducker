from rest_framework import viewsets
from .serializers import LogSerializer, ConnectionSerializer, PayloadSerializer
from .models import Log, Payload
from connections.models import Connection
from django_filters.rest_framework import DjangoFilterBackend


# class ScriptViewSet(viewsets.ModelViewSet):
#     serializer_class = ScriptSerializer
#     queryset = Script.objects.all()


class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    queryset = Log.objects.all()


class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()


class PayloadViewSet(viewsets.ModelViewSet):
    serializer_class = PayloadSerializer
    queryset = Payload.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payload']