from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, LoginForm, RegisterForm
from .models import File, SharedFile, FileIntegrity
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from .forms import ShareFileForm
from django.core.exceptions import ValidationError


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
    return redirect(reverse('file_app:login'))

# Can view the files for the user
@login_required
def profile(request):
    # Get files uploaded by the current user
    user_files = File.objects.filter(owner=request.user)
 # Get files shared with the current user
    shared_files = SharedFile.objects.filter(user=request.user).values('file')

    # Filter the File model to get shared files
    files = File.objects.filter(Q(owner=request.user) | Q(id__in=shared_files))

    context = {
        'files': files,
    }

    return render(request, "profile.html", context)

# Here you will be able to upload a file for that user
@login_required
@csrf_protect
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # Handle checking file integrity here and create file object to save after checking
        if form.is_valid():
            try:
                # Check if a shared file entry with the same user and file already exists
                file_instance = File.objects.create(
                    owner=request.user,
                    file=form.cleaned_data['file'],
                    file_name=form.cleaned_data['title'],
                    file_size=form.cleaned_data['file'].size
                )
                #file_instance = File(file=request.FILES["file"])
                file_instance.save()
                messages.success(request, f'File is successfully uploaded.')
                return redirect(reverse('file_app:profile')) # go back to profile page to see all the files
            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})

@login_required
def share_file(request, file_id):
    # Get the file object using the file_id
    file_to_share = get_object_or_404(File, id=file_id)

    # Check if the file's owner is the current user
    if file_to_share.owner != request.user:
        messages.error(request, "You can only share your own files.")
        return redirect('file_app:profile')
    

    if request.method == 'POST':
        form = ShareFileForm(request, request.POST)
        if form.is_valid():
            user_to_share = form.cleaned_data['shared_user']
            permission = form.cleaned_data['permission']
            user_to_share = form.cleaned_data['shared_user']
            permission = form.cleaned_data['permission']
            
            # Check if the file's owner is the current user
            if file_to_share.owner != request.user:
                messages.error(request, "You can only share your own files.")
                return redirect('file_app:profile')

             # Check if a shared file entry with the same user and file already exists
            shared_file, created = SharedFile.objects.get_or_create(
                user=user_to_share,
                file=file_to_share,
                defaults={'permission': permission, 'file_name': file_to_share.file_name}
            )

            if not created:
                # Update the existing entry with a new permission
                shared_file.permission = permission
                shared_file.save()
                
            messages.success(request, f"File '{file_to_share.file_name}' has been shared with {user_to_share.username}.")
    else:
        form = ShareFileForm(request)
    # In the template, we should list users and provide a way to select a user to share the file with
    users = User.objects.exclude(id=request.user.id)
    context = {
        'file': file_to_share,
        'users': users,
        'form': form,
    }

    return render(request, 'share_file.html', context)
