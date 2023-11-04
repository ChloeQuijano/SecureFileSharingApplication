from django.contrib import admin
from django.urls import path, include 
from . import views

app_name = 'file_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('upload_file/', views.upload_file, name='upload_file'),
]
