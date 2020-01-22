from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.urls import reverse
from connections.models import Connection, TerminalData, ScriptData
from payloads.models import Payload, TerminalLog, ScriptLog, TerminalHistory
from django.contrib.auth.models import User
import hashlib


class ConnectionTestCase(TestCase):
    def setUp(self):
        payload = Payload.objects.create(payload_name='test_name', payload_description='test_description',
                                         payload='test_payload')
        connection = Connection.objects.create(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2", name="test_name",
                                               description="test_description", ip="0.0.0.0", status=True)
        terminal_log = TerminalLog.objects.create(connection=connection, content='test_content',
                                                  current_directory='test_current_directory')
        script_log = ScriptLog.objects.create(payload=payload, connection=connection, content='test_content')
        terminal_history = TerminalHistory.objects.create(connection=connection, command='test_command')
        terminal_data = TerminalData.objects.create(input="test_terminal_data_input", connection_id=connection)
        script_data = ScriptData.objects.create(input='test_script_data_input', connection_id=connection,
                                                payload_name='test_payload_name')
        normal_user = User.objects.create_user(username='test_user', email='test_email@email.com', password='test_password')

    def test_data_integrity_connections(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        terminal_data = TerminalData.objects.get(input="test_terminal_data_input")
        script_data = ScriptData.objects.get(input='test_script_data_input')
        self.assertEqual(terminal_data.connection_id, connection)
        self.assertEqual(script_data.connection_id, connection)

    def test_homepage_login(self):
        client = Client()
        response_get = client.get('/')
        self.assertEqual(response_get.status_code, 200)
        test_user = User.objects.get(username='test_user')
        response_post = client.post('/', {'username': test_user.username, 'password': test_user.password})
        self.assertEqual(response_post.status_code, 200)

    def test_register(self):
        client = Client()
        response_get = client.get('/register')
        self.assertEqual(response_get.status_code, 200)
        post = {'username': 'new_user', 'password': 'new_password', 'password_again': 'new_password', 'email':'new_email@email.com'}
        response_post = client.post('/register', post)
        self.assertEqual(response_post.status_code, 302)

    def test_installation_files(self):
        client = Client()
        response_get = client.get('/installation/digistump_installation')
        self.assertEqual(response_get.get('Content-Disposition'),
                         "attachment; filename=arduino-cli_0.6.0_Windows_64bit.zip")

    def test_installation_page_unauthorized(self):
        client = Client()
        response_get = client.get('/installation')
        self.assertEqual(response_get.status_code, 302)

    def test_connections_page_unauthorized(self):
        client = Client()
        response_get = client.get('/connections')
        self.assertEqual(response_get.status_code, 302)

    def test_scripts_page_unauthorized(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        client = Client()
        response_get = client.get(f'/connections/{str(connection.uuid).upper()}/scripts')
        self.assertEqual(response_get.status_code, 302)

    def test_terminal_page_unauthorized(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        client = Client()
        response_get = client.get(f'/connections/{str(connection.uuid).upper()}/details')
        self.assertEqual(response_get.status_code, 302)

    def test_details_page_unauthorized(self):
        connection = Connection.objects.get(uuid="8bb5a620-6554-4081-9dc2-e2dbc23bd8c2")
        client = Client()
        response_get = client.get(f'/connections/{str(connection.uuid).upper()}/terminal')
        self.assertEqual(response_get.status_code, 302)

    