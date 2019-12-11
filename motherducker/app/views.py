from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'index.html'

class ConnectionsView(TemplateView):
    template_name = 'connections.html'

class TerminalView(TemplateView):
    template_name = 'terminal.html'

class ScriptsView(TemplateView):
    template_name = 'scripts.html'

class ConnectionDetailsView(TemplateView):
    template_name = 'connection_details.html'