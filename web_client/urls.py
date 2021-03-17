from django.urls import path

from . import views
from . import mutation_view

urlpatterns = [
    path('', views.index, name='index'),
    path('mutation/', mutation_view.index, name='mutation'),
]