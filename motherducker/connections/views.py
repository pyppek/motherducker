from mimetypes import guess_type

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from payloads.models import Payload
from .models import Connection


class HomePageView(TemplateView):
    template_name = 'index.html'


class InstallationView(TemplateView):
    template_name = 'installation.html'

    # TODO put the payload to make the connection in this zip in connection_script.ino
    def download_digistump_installation(request):
        file_path = './connections/install_files/arduino-cli_0.6.0_Windows_64bit.zip'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f, content_type=guess_type(file_path)[0])
            response['Content-Disposition'] = 'attachment; filename=arduino-cli_0.6.0_Windows_64bit.zip'
            response['Content-Length'] = len(response.content)
            return response


class ConnectionsView(TemplateView):
    template_name = 'connections.html'

    def get(self, request, *args, **kwargs):
        context = super(ConnectionsView, self).get_context_data(**kwargs)
        context['connections'] = Connection.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {'connections': Connection.objects.all()}
        print(request.POST.get('connection'))
        return render(request, self.template_name, context)


class TerminalView(TemplateView):
    template_name = 'terminal.html'

    def get(self, request, *args, **kwargs):
        context = {}
        # TODO change this so it picks it up through reverse shell which folder user resides in
        context['terminal'] = 'C:\\>'
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        # TODO change this so it picks it up through reverse shell which folder user resides in
        context['terminal'] = 'C:\\>'
        print(f"Your terminal input was: {request.POST.get('terminal_input')}")
        return render(request, self.template_name, context)


class ScriptsView(TemplateView):
    template_name = 'scripts.html'

    def get(self, request, *args, **kwargs):
        context = super(ScriptsView, self).get_context_data(**kwargs)
        context['payloads'] = Payload.objects.all()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {'payloads': Payload.objects.all()}
        print(request.POST.get('payload'))
        return render(request, self.template_name, context)


class ConnectionDetailsView(TemplateView):
    template_name = 'connection_details.html'