from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('exit/', views.exit, name='exit'),

    path('teams/<int:team_pk>', views.teams, name='teams'),
    path('create_team/', views.create_team, name='create_team'),
    path('get_in_team/<int:team_pk>', views.get_in_team, name='get_in_team'),

    path('make_done_tasks/<int:team_pk>', views.make_done_tasks, name='make_done_tasks'),
    path('add_task/<int:team_pk>', views.add_task, name='add_task'),

    path('', views.index, name='index')
]