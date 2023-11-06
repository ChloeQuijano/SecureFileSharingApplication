from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, LoginForm, RegisterForm
from .models import File, SharedFile, FileIntegrity
from django.contrib.auth.models import User

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
    # users = User.objects.exclude(id=request.user.id)  # Get all users except the current user
    context = {
        'files': files,
        # 'users': users,  # Add the list of users to the context
    }
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

@login_required
def share_file(request, file_id):
    # Get the file object using the file_id
    file = get_object_or_404(File, id=file_id)  # Fetch the file object
    users = User.objects.exclude(id=request.user.id)  # Fetch the list of users excluding the current user

    # Check if the file's owner is the current user
    if file.owner != request.user:
        messages.error(request, "You can only share your own files.")
        return redirect('file_app:profile')

    if request.method == 'POST':
        # Retrieve the selected user's ID from the form
        selected_user_id = request.POST.get('shared_user')
        # user_to_share = User.objects.filter(id=selected_user_id).first()
        #TODO: MORE STUFF TO ADD
    context = {
        'file': file,
        'users': users,
    }

    return render(request, 'share_file.html', context)
