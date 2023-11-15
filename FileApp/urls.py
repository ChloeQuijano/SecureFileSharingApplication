"""
Here is where the urls for routing in our app happens
"""
from django.urls import path
from . import views

app_name = 'file_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.client_login, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('share_file/<int:file_id>/', views.share_file, name='share_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file')
]
