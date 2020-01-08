from rest_framework import serializers
from .models import Log, Payload
from connections.models import Connection


# class ScriptSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Script
#         fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'

    def create(self, validated_data):
        print(self.data.get('payload'))
        uuid = validated_data.pop('connection')
        payload = validated_data.pop('payload')
        content = validated_data.pop('content')
        print('hi')
        print(uuid)
        print(payload)
        print(content)

        connection, _ = Connection.objects.get_or_create(uuid=uuid.uuid)
        payloads, _ = Payload.objects.get_or_create(payload_name=payload)
        log = Log.objects.create(connection=connection, payload=payloads, content=content)
        return log


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'


class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = '__all__'