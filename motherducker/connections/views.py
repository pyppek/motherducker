from mimetypes import guess_type
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from payloads.models import Payload, TerminalLog, ScriptLog, TerminalHistory
from .models import Connection, ScriptData, TerminalData
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
import time


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.session['session']['username'] and request.session['session']['password']:
                request.session.flush()
        except KeyError:
            pass
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            data = {"username": username, "password":password}
            request.session['session'] = data
            return redirect('installation')
        else:
            context['wrong_password'] = 'E-mail or password is incorrect'
            return render(request, self.template_name, context)


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

    def get(self, request, *args, **kwargs):
        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = {'username': request.session['session']['username']}
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')


class ConnectionsView(TemplateView):
    template_name = 'connections.html'

    def get(self, request, *args, **kwargs):
        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = super(ConnectionsView, self).get_context_data(**kwargs)
                context['connections'] = Connection.objects.all()
                context['username'] = request.session['session']['username']
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')


    def post(self, request, *args, **kwargs):
        context = {'connections': Connection.objects.all()}
        return render(request, self.template_name, context)


class TerminalView(TemplateView):
    template_name = 'terminal.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        time.sleep(3)
        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = {'username': request.session['session']['username']}
                context['terminal'] = 'C:\\>'
                context['uuid'] = self.kwargs.get('uuid')
                context['history'] = TerminalHistory.objects.filter(connection=self.kwargs.get('uuid'))
                get_uuid = Connection.objects.get(uuid=self.kwargs.get('uuid'))
                try:
                    terminal_data = TerminalLog.objects.filter(connection=get_uuid).latest('id')
                    context['terminal'] = terminal_data.current_directory
                    context['terminal_output'] = terminal_data.content
                    context['terminal_history'] = TerminalLog.objects.filter(connection=get_uuid)
                except:
                    pass
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        context = {}
        context['terminal'] = 'C:\\>'
        context['uuid'] = self.kwargs.get('uuid')
        get_uuid = Connection.objects.get(uuid=self.kwargs.get('uuid'))

        input = request.POST.get('terminal_input')
        context['history'] = TerminalHistory.objects.filter(connection=get_uuid)

        try:
            terminal_data = TerminalLog.objects.filter(connection=get_uuid).latest('id')
            context['terminal'] = terminal_data.current_directory
            context['terminal_output'] = terminal_data.content
            TerminalData.objects.all().delete()
            TerminalData.objects.create(input=input,
                                        connection_id=get_uuid)
        except:
            TerminalData.objects.all().delete()
            TerminalData.objects.create(input=input,
                                        connection_id=get_uuid)

        TerminalHistory.objects.create(command=input,
                                       connection=get_uuid)

        # TODO also delete terminal history when connection is lost or after a day or something?
        # only keep the most recent 6 lines from the terminal history (delete older ones)
        if TerminalHistory.objects.filter(connection=get_uuid).count() > 5:
            max_datetime = TerminalHistory.objects.order_by('-timestamp')[5]
            delete_older = TerminalHistory.objects.filter(timestamp__lt=max_datetime.timestamp)
            delete_older.delete()

        return TerminalView.get(self, request, *args, **kwargs)


class ScriptsView(TemplateView):
    template_name = 'scripts.html'

    def get(self, request, *args, **kwargs):

        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = super(ScriptsView, self).get_context_data(**kwargs)
                context['payloads'] = Payload.objects.all()
                context['username'] = request.session['session']['username']
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')


    def post(self, request, *args, **kwargs):
        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = {'username': request.session['session']['username']}
                context['payloads'] = Payload.objects.all()
                context['uuid'] = self.kwargs.get('uuid')
                get_uuid = Connection.objects.get(uuid=self.kwargs.get('uuid'))
                ScriptData.objects.all().delete()
                ScriptData.objects.create(input=request.POST.get('payload'),
                                          payload_name=request.POST.get('payload_name'),
                                          connection_id=get_uuid)
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')


class ConnectionDetailsView(TemplateView):
    template_name = 'connection_details.html'

    def get(self, request, *args, **kwargs):
        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = super(ConnectionDetailsView, self).get_context_data(**kwargs)
                context['username'] = request.session['session']['username']
                context['uuid'] = self.kwargs.get('uuid')
                context['connection'] = Connection.objects.get(uuid=context['uuid'])
                context['terminal_log'] = TerminalLog.objects.filter(connection=context['connection'])
                context['script_log'] = ScriptLog.objects.filter(connection=context['connection'])
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')

    def post(self, request, *args, **kwargs):

        try:
            username = request.session['session']['username']
            password = request.session['session']['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                context = {'username': request.session['session']['username']}
                context['uuid'] = self.kwargs.get('uuid')
                return render(request, self.template_name, context)
            else:
                return redirect('home')
        except KeyError:
            return redirect('home')


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if request.POST.get('password_again') == password:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('home')
            except:
                context['wrong_password'] = "Passwords do not match!"
                return render(request, self.template_name, context)
        else:
            context['wrong_password'] = "Passwords do not match!"
            return render(request, self.template_name, context)