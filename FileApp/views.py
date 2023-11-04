from django.shortcuts import render
from django.http import HttpResponse

# TODO: Make home page where navigation bar contains sign up / login
def home(request):
    return HttpResponse("This is the home page")

# TODO: Register a new user account page
def register(request):
    return HttpResponse("This is the register page")

# TODO: Login page for user
def login(request):
    return HttpResponse("This is the login page")

# TODO: Logout page for user
def logout(request):
    return HttpResponse("This is the logout page")

# TODO: After login, can view the files for the user
def profile(request):
    return HttpResponse("This is the profile page")

# TODO: Here you will be able to upload a file for that user
def upload_file(request):
    return HttpResponse("This is the upload file page")