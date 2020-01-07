from django.urls import path
from .views import HomePageView, ConnectionsView, ScriptsView, ConnectionDetailsView, TerminalView, InstallationView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('installation', InstallationView.as_view(), name='installation'),
    path('installation/digistump_installation', InstallationView.download_digistump_installation, name='digistump_installation'),
    path('connections', ConnectionsView.as_view(), name='connections'),
    path('connections/<slug:uuid>/terminal', TerminalView.as_view(), name='terminal'),
    path('connections/<slug:uuid>/scripts', ScriptsView.as_view(), name='scripts'),
    path('connections/<slug:uuid>/details', ConnectionDetailsView.as_view(), name='details'),
]