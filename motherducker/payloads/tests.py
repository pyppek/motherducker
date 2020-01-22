from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from connections.models import Connection, TerminalData, ScriptData
from payloads.models import Payload, TerminalLog, ScriptLog, TerminalHistory


class PayloadTestCase(TestCase):
    def setUp(self):
        payload = Payload.objects.create(payload_name='test_name', payload_description='test_description', payload='test_payload')
        connection = Connection.objects.create(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2", name="test_name",
                                               description="test_description", ip="0.0.0.0", status=True)
        terminal_log = TerminalLog.objects.create(connection=connection, content='test_content',
                                                  current_directory='test_current_directory')
        script_log = ScriptLog.objects.create(payload=payload, connection=connection, content='test_content')
        terminal_history = TerminalHistory.objects.create(connection=connection, command='test_command')
        terminal_data = TerminalData.objects.create(input="test_terminal_data_input", connection_id=connection)
        script_data = ScriptData.objects.create(input='test_script_data_input', connection_id=connection,
                                                payload_name='test_payload_name')

    def test_data_integrity_payloads(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        payload = Payload.objects.get(payload_name='test_name')
        terminal_log = TerminalLog.objects.get(content='test_content')
        script_log = ScriptLog.objects.get(content='test_content')
        terminal_history = TerminalHistory.objects.get(command='test_command')
        self.assertEqual(payload, script_log.payload)
        self.assertEqual(connection, script_log.connection)
        self.assertEqual(connection, terminal_history.connection)
        self.assertEqual(connection, terminal_log.connection)

    def test_backdoor_api(self):
        connection_uuid = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2").uuid
        script_payload = ScriptData.objects.get(input='test_script_data_input')
        client = Client()
        response = client.get(f'/payloads/backdoor_api/{connection_uuid}')
        json = response.json()
        self.assertEqual(json['active'], True)
        self.assertEqual(json['uuid'], str(connection_uuid).upper())
        self.assertEqual(json['payload'], script_payload.input)
        self.assertEqual(json['payload_name'], script_payload.payload_name)
        self.assertEqual(json['terminal'], False)

    def test_terminal_api(self):
        connection_uuid = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2").uuid
        terminal_input = TerminalData.objects.get(input="test_terminal_data_input")
        client = Client()
        response = client.get(f'/payloads/terminal_api/{connection_uuid}')
        json = response.json()
        self.assertEqual(json['active'], True)
        self.assertEqual(json['uuid'], str(connection_uuid).upper())
        self.assertEqual(json['input'], terminal_input.input)
        self.assertEqual(json['terminal'], True)