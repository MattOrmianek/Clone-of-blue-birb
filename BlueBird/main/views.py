from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username = username)
        except Exception as e:
            messages.error(request, "User does not exist.")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or password is incorrect.")
    context = {'page': page}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')

def registerUser(request):
    form = UserCreationForm
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home.html')
        else:
            messages.error(request, "An error occured during registartion.")

    return render(request, 'login.html', context)

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__contains = q) | Q(name__icontains = q) | Q(description__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'home.html', context)

def room(request, pk):
    room_number = Room.objects.get(id = pk)
    context = {'room': room_number}
    return render(request, 'room.html', context)

@login_required(login_url = 'login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
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