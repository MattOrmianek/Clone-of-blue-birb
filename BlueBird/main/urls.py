from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    path('register/', views.registerUser, name = "register"),
    path('room/<str:pk>', views.room, name = "room"),
    path('create-room/', views.create_room, name = "create-room"),
    path('update-room/<str:pk>/', views.update_room, name = "update-room"),
    path('delete-room/<str:pk>/', views.delete_room, name = "delete-room")
]
