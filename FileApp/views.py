from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, LoginForm, RegisterForm
from .models import File

# Home page where navigation bar contains sign up / login links
def home(request):
    return render(request, "home.html")

# Register a new user account page
def register(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {'form': form})
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # TODO: check that inputs are valid for saving a new user model
            return HttpResponse("Successful registration")
        else:
            return render(request, 'register.html', {'form': form})

# Login page for user
def login(request):
    if request.method == "GET":
        # FIXME: need to check if already logged in and don't need to redo login
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    
    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # TODO: create User authentication
            messages.success(request,f'Hi {user.username.title()}, welcome back!')
        
        # if error occurs 
        messages.error(request,f'Invalid username or password')
        return render(request, "login.html", {'form': form})

# Logout page for user
def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return render(request, "login.html")

# Can view the files for the user
@login_required
def profile(request):
    # FIXME: Need to get files ONLY for that user, if not logged in, will prompt user to login instead
    # Fixed - if not logged in it will redirect them to the login page (LOGIN_URL added in settings.py) - M
    files = File.objects.filter(owner=request.user)
    context = {'files': files}
    return render(request, "profile.html", context)

# TODO: Here you will be able to upload a file for that user
@login_required
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        #TODO: Handle checking file integrity here and create file object to save after checking
        if form.is_valid():
            # TODO: need to make inputs correct for creating file object
            # file_instance = File(file=request.FILES["file"])
            # file_instance.save()
            return HttpResponse("Successful upload")
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})