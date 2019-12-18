from django.urls import path
from .views import HomePageView, ConnectionsView, ScriptsView, ConnectionDetailsView, TerminalView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('connections', ConnectionsView.as_view(), name='connections'),
    path('connections/terminal', TerminalView.as_view(), name='terminal'),
    path('connections/scripts', ScriptsView.as_view(), name='scripts'),
    path('connections/details', ConnectionDetailsView.as_view(), name='details'),
]