from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Team, Membership, Task

def register(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if not (user is None):
        login(request, user)
    else:
        try:
            usr = User.objects.get(username=username)
        except:
            u = User.objects.create_user(username, username, password)
            u.save()
            login(request, u)
            
    return redirect('index')
    
def exit(request):
    logout(request)
    return redirect('index')

def index(request):
    if request.user.is_authenticated:
        pk = request.user.pk
        teams_list = []
        memberships = Membership.objects.all().values().filter(user_id=pk)
        for ship in list(memberships):
            teams_list.append(Team.objects.get(pk=ship['team_id']))
        other_teams_list = list(set(Team.objects.all()) - set(teams_list))
        context = { 'auth': request.user.is_authenticated, 'list' : teams_list, 'other_teams_list' : other_teams_list }
        return render(request, 'mainapp\\index.html', context)
    else:
        context = { 'auth': request.user.is_authenticated }
        return render(request, 'mainapp\\index.html', context)

def create_team(request):

    team = Team.objects.create(name=request.POST['name'], creator=request.user)
    team.save()

    return redirect('get_in_team', team_pk=team.pk)

def get_in_team(request, team_pk):

    mmbshp = Membership.objects.create(user=request.user, team=Team.objects.get(pk=team_pk))
    mmbshp.save()

    return redirect('teams', team_pk=team_pk)

def teams(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)

    memberships = Membership.objects.filter(team=team)

    my_memb = Membership.objects.get(user=request.user)
    tasks = Task.objects.filter(membership=my_memb, is_done=False)

    return render(request, 'mainapp\\team.html', {'team' : team, 'memberships' : memberships, 'tasks' : tasks})

def make_done_tasks(request, team_pk):

    # Вот такое стоит делать AJAX-запросами

    for val in request.POST:
        if request.POST[val] == 'on':
            task = Task.objects.get(pk=int(val))
            task.is_done = True
            task.save()

    return redirect('teams', team_pk=team_pk)

def add_task(request, team_pk):
    to_membership_pk = request.POST['to_membership']
    title = request.POST['title']
    text = request.POST['text']

    task = Task.objects.create(membership=Membership.objects.get(pk=int(to_membership_pk)), title=title, text=text)
    task.save()

    return redirect('teams', team_pk=team_pk)