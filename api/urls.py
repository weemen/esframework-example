from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game_handler', views.game_handler, name='game_handler'),
    path('game_status', views.game_status, name='game_status'),
]