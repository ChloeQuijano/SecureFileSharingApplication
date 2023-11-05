from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, LoginForm, RegisterForm
from .models import File

from .userauth import *

# Home page where navigation bar contains sign up / login links
def home(request):
    return render(request, "home.html")

# Register a new user account page
@csrf_protect
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            psw2 = form.cleaned_data["password2"]

            try:
                reg = UserRegistration(username, email, password, psw2)
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username is already in use")
                    return render(request, "register.html", {"form": form})
                if not reg.is_email_valid():
                    messages.error(request, "Email is invalid format")
                    return render(request, "register.html", {"form": form})
                if not reg.is_password_strong():
                    messages.error(request, "Password is not strong enough ")
                    return render(request, "register.html", {"form": form})
                if not reg.are_passwords_matching():
                    messages.error("Passwords are not matching")
                    return render(request, "register.html", {"form": form})
                elif reg.is_email_valid() and reg.is_password_strong()  and reg.are_passwords_matching():
                    hashed = reg.hash_password()
                    user = User(username=username, email=email, password=hashed.decode('utf-8'))
                    user.save()
                    messages.success(request,"Successful registration" )
                    return redirect(reverse('file_app:home'))

            except Exception as e:
                    messages.error(request, str(e))
        else:
            messages.error(request, "Form is invalid. Please check your input.")
    else:
            form = RegisterForm()
    return render(request, "register.html", {'form': form})

# Login page for user
@csrf_protect
def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    auth_login(request, user)
                    messages.success(request, f"Hi {user.username.title()}, welcome back!")
                    return redirect(reverse('file_app:home'))  # Redirect to a secured page after successful login
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "User does not exist")

    # Handle GET request or form errors
    return render(request, "login.html", {"form": form})


# Logout page for user
@csrf_protect
def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return render(request, "login.html")

# Can view the files for the user
@login_required
def profile(request):
    # FIXME: Need to get files ONLY for that user, if not logged in, will prompt user to login instead
    files = File.objects.all()
    context = {'files': files}
    return render(request, "profile.html", context)

# TODO: Here you will be able to upload a file for that user
@login_required
@csrf_protect
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
