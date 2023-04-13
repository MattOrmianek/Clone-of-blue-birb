from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.

#rooms = [
#    {'id': 1, 'name': 'First room'},
#    {'id': 2, 'name': 'Second room'},
#    {'id': 3, 'name': 'Third room'},
#    {'id': 4, 'name': 'Fourth room'}
#]


def index(request):
    #return HttpResponse("<h1> Response from views.py </h1>")
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'home.html', context)

def room(request, pk):
    #return HttpResponse('ROOM')
    room_number = Room.objects.get(id = pk)
    context = {'room': room_number}
    return render(request, 'room.html', context)

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

def update_room(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance = room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {'form': form}
    return render(request, 'room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')

    return render(request, 'delete.html', {'obj':room})