from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = 'index.html'


class ConnectionsView(TemplateView):
    template_name = 'connections.html'


class TerminalView(TemplateView):
    template_name = 'terminal.html'

    def get(self, request, *args, **kwargs):
        context = {}
        # TODO change this so it picks it up through reverse shell which folder user resides in
        context['terminal'] = 'C:\\>'
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        context = {}
        # TODO change this so it picks it up through reverse shell which folder user resides in
        context['terminal'] = 'C:\\>'
        return render(request, self.template_name, context)


class ScriptsView(TemplateView):
    template_name = 'scripts.html'


class ConnectionDetailsView(TemplateView):
    template_name = 'connection_details.html'