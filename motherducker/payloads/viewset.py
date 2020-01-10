from rest_framework import viewsets
from .serializers import ScriptLogSerializer, TerminalLogSerializer, ConnectionSerializer, PayloadSerializer
from .models import ScriptLog, TerminalLog, Payload
from connections.models import Connection
from django_filters.rest_framework import DjangoFilterBackend


class ScriptLogViewSet(viewsets.ModelViewSet):
    serializer_class = ScriptLogSerializer
    queryset = ScriptLog.objects.all()


class TerminalLogViewSet(viewsets.ModelViewSet):
    serializer_class = TerminalLogSerializer
    queryset = TerminalLog.objects.all()


class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionSerializer
    queryset = Connection.objects.all()


class PayloadViewSet(viewsets.ModelViewSet):
    serializer_class = PayloadSerializer
    queryset = Payload.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['payload', 'payload_name']