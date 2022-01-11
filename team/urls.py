from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.team, name='team'),
]