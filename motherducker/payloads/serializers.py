from rest_framework import serializers
from .models import ScriptLog, TerminalLog, Payload
from connections.models import Connection


class ScriptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptLog
        fields = '__all__'

    def create(self, validated_data):
        uuid = validated_data.pop('connection')
        payload = validated_data.pop('payload')
        content = validated_data.pop('content')

        connection, _ = Connection.objects.get_or_create(uuid=uuid.uuid)
        payloads, _ = Payload.objects.get_or_create(payload_name=payload)
        if ScriptLog.objects.filter(payload=payloads, connection=connection).exists():
            return ScriptLog.objects.get(connection=connection, payload=payloads)
        script_log, _ = ScriptLog.objects.get_or_create(connection=connection, payload=payloads, content=content)
        return script_log


class TerminalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalLog
        fields = '__all__'

    def create(self, validated_data):
        uuid = validated_data.pop('connection')
        content = validated_data.pop('content')
        current_dir = validated_data.pop('current_directory')
        connection, _ = Connection.objects.get_or_create(uuid=uuid.uuid)
        terminal_log, _ = TerminalLog.objects.update_or_create(connection=connection, content=content, current_directory=current_dir)
        return terminal_log


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'


class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = '__all__'
