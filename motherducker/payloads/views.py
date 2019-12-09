from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from mimetypes import guess_type


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def download_payload(request):
    file_path = './payloads/Reverse_shell.ps1'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type=guess_type(file_path)[0])
        response['Content-Disposition'] = 'attachment; filename=Reverse_shell.ps1'
        response['Content-Length'] = len(response.content)
        return response

