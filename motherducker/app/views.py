from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from payloads.models import Payload


class HomePageView(TemplateView):
    template_name = 'index.html'

class ConnectionsView(TemplateView):
    template_name = 'connections.html'

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