from django.test import TestCase
from connections.models import Connection
from payloads.models import Payload, TerminalLog, ScriptLog, TerminalHistory

class PayloadTestCase(TestCase):
    def setUp(self):
        payload = Payload.objects.create(payload_name='test_name', payload_description='test_description', payload='test_payload')
        connection = Connection.objects.create(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2", name="test_name",
                                               description="test_description", ip="0.0.0.0", status=True)
        script_log = ScriptLog.objects.create(payload=payload, connection=connection, content='test_content')

    def test_data_integrity_payloads(self):
        payload = Payload.objects.get(payload_name='test_name')
        script_log = ScriptLog.objects.get(content='test_content')
        self.assertEqual(payload, script_log.payload)
