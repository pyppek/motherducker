from django.http import HttpResponse
from django.views.generic import TemplateView
from payloads.models import Payload


class HomePageView(TemplateView):
    template_name = 'index.html'

class ConnectionsView(TemplateView):
    template_name = 'connections.html'

class ScriptsView(TemplateView):
    template_name = 'scripts.html'

    def get_context_data(self, **kwargs):
        context = super(ScriptsView, self).get_context_data(**kwargs)
        context['payloads'] = Payload.objects.all()
        return context

class ConnectionDetailsView(TemplateView):
    template_name = 'connection_details.html'