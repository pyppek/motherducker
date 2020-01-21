from django.test import TestCase
from connections.models import Connection, TerminalData, ScriptData


class ConnectionTestCase(TestCase):
    def setUp(self):
        connection = Connection.objects.create(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2", name="test_name",
                                               description="test_description", ip="0.0.0.0", status=True)
        terminal_data = TerminalData.objects.create(input="test_terminal_data_input", connection_id=connection)
        script_data = ScriptData.objects.create(input='test_script_data_input', connection_id=connection,
                                                payload_name='test_payload_name')

    def test_data_integrity_connections(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        terminal_data = TerminalData.objects.get(input="test_terminal_data_input")
        script_data = ScriptData.objects.get(input='test_script_data_input')
        self.assertEqual(terminal_data.connection_id, connection)
        self.assertEqual(script_data.connection_id, connection)