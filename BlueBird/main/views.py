from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

#rooms = [
#    {'id': 1, 'name': 'First room'},
#    {'id': 2, 'name': 'Second room'},
#    {'id': 3, 'name': 'Third room'},
#    {'id': 4, 'name': 'Fourth room'}
#]

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User does not exist.")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect.")
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def index(request):
    #return HttpResponse("<h1> Response from views.py </h1>")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__contains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'home.html', context)

def room(request, pk):
    #return HttpResponse('ROOM')
    room_number = Room.objects.get(id = pk)
    context = {'room': room_number}
    return render(request, 'room.html', context)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url = 'login')
def update_room(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        return HttpResponse("You are not authorized to view this page.")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form': form}
    return render(request, 'room_form.html', context)

@login_required(login_url = 'login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not authorized to view this page.")

    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'delete.html', {'obj':room})