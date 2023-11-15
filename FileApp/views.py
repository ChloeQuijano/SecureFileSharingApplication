"""
Contains all the views for the app here
"""
import logging
import hashlib
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as server_login,logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from FileApp.fileencrypt import *
from .forms import UploadFileForm, LoginForm, RegisterForm, ShareFileForm
from .models import File, SharedFile, FileIntegrity
from .userauth import *
from .filevalidate import has_permission
from .fernet import get_fernet_key

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def home(request):
    """
    Home page where navigation bar contains sign up / login links
    """
    return render(request, "home.html")

@csrf_protect
def register(request):
    """
    Register a new user account page
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Sanitize input
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            psw2 = form.cleaned_data["password2"]

            try:
                reg = UserRegistration(username, email, password, psw2)
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username is already in use")
                elif not reg.is_email_valid():
                    messages.error(request, "Email is invalid format")
                elif not reg.is_password_strong():
                    messages.error(request, "Password is not strong enough ")
                elif not reg.is_username_valid():
                    messages.error(request, "Username is not valid, must be alphanumeric and underscores ")
                elif not reg.are_passwords_matching():
                    messages.error("Passwords are not matching")
                else:
                    # passes all validations
                    hashed = reg.hash_password()
                    user = User(username=username, email=email, password=hashed.decode('utf-8'))
                    user.save()

                    messages.success(request,"Successful registration" )
                    server_login(request, user)
                    return redirect(reverse('file_app:home'))

                # all renders the form
                return render(request, "register.html", {"form": form})

            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Form is invalid. Please check your input.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {'form': form})

@csrf_protect
def client_login(request):
    """
    Login page for user
    """
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            # Sanitize input
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    server_login(request, user)
                    messages.success(request, f"Hi {user.username.title()}, welcome back!")
                    # Redirect to the user's file page
                    return redirect(reverse('file_app:profile'))
                else:
                    messages.error(request, "Invalid username or password")
            else:
                messages.error(request, "User does not exist")

    # Handle GET request or form errors
    return render(request, "login.html", {"form": form})

@csrf_protect
@login_required
def sign_out(request):
    """
    Sign out page where user is logged out. Redirects logout user to login page
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('file_app:login'))

@login_required(login_url='file_app:login')
def profile(request):
    """
    Profile page where all files are listed. Login required to access page
    """
    # Get files shared with the current user
    shared_files = SharedFile.objects.filter(user=request.user).values('file')

    # Filter the File model to get shared files
    files = File.objects.filter(Q(owner=request.user) | Q(id__in=shared_files))

    # Zip the permission with the file  -- Anne
    files_with_permission = [{'file': file, 'has_permission': has_permission(file, request.user)} for file in files]

    context = {
        'files': files_with_permission,
    }

    return render(request, "profile.html", context)

@login_required(login_url='file_app:login')
@csrf_protect
def upload_file(request):
    """
    Upload file form and page. Login required to access page
    """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        # Handle checking file integrity here and create file object to save after checking
        if form.is_valid():
            try:
                # checks if file title already exists for the user
                if File.objects.filter(owner=request.user, file_name=form.cleaned_data['title']).exists() or SharedFile.objects.filter(user=request.user, file__file_name = form.cleaned_data['title']).exists():
                    messages.error(request, "Title for file already exists in database. Please input a new title")
                    return render(request, "upload_file.html", {"form": form})

                key_string = get_fernet_key()
                encryptor = FileEncryptor(key_string)
                file = form.cleaned_data['file']

                # Read the content from the file     
                file.seek(0,0)
                file_content =file.read()

                # Calculate hash digest of file before saving
                hash_bfr_save = file_hashing(file_content)
                file.seek(0,0)
                encrypted_file = encryptor.file_encrypt(file)

                file_instance = File.objects.create(
                    owner=request.user,
                    file=encrypted_file,
                    file_name=form.cleaned_data['title'],
                    file_size=form.cleaned_data['file'].size,
                    file_key = key_string
                )

                # Saves the file object to database
                file_instance.save()

                # Calculate hash digest of file after saving
                decrypted_saved_file = encryptor.file_decrypt(file_instance.file)
                decrypted_saved_file.seek(0,0)
                decrypted_content = decrypted_saved_file.read()
                hash_after_save = file_hashing(decrypted_content)

                if hash_after_save == hash_bfr_save:
                    messages.success(request, 'File is successfully uploaded.')
                    intergrity = FileIntegrity(file=file_instance, sha256_hash=hash_after_save)
                    intergrity.save()
                    return redirect(reverse('file_app:profile')) # go back to profile page to see all the files
                else:
                    # Delete corrupted file
                    file_instance.delete()
                    messages.error(request, "File integrity compromised during upload, try again")

            except ValidationError as e:
                messages.error(request, e.message)
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})

@login_required(login_url='file_app:login')
@csrf_protect
def share_file(request, file_id):
    """
    Share file form and page. Login required to access page
    """
    try:
        # Get the file object using the file_id
        file_to_share = get_object_or_404(File, id=file_id)

        # Check if the file's owner is the current user
        if file_to_share.owner != request.user:
            messages.error(request, "You can only share your own files.")
            return redirect('file_app:profile')

        if request.method == 'POST':
            try:
                form = ShareFileForm(request, request.POST)
                if form.is_valid():
                    # sanatized user input
                    user_to_share = form.cleaned_data['shared_user']
                    permission = form.cleaned_data['permission']

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
                        messages.success(request,f"File '{file_to_share.file_name}' has successfully been updated for {user_to_share.username}.")
                    else:
                        # Add comment to user - Anne
                        messages.success(request,f"File '{file_to_share.file_name}' has successfully been shared with {user_to_share.username}.")
            except Exception as e:
                messages.error(request, f"An error occurred while processing the form: {str(e)}")
                # We may want to log the exception for further analysis
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

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        # We may want to log the exception for further analysis
        return redirect('file_app:profile')

@login_required
def download_file(request, file_id):
    """
    Download the file for the user. Login required to access function
    """
    try:
        file_obj = get_object_or_404(File, id=file_id)
        encryptor = FileEncryptor(file_obj.file_key)
        decrypted_file = encryptor.file_decrypt(file_obj.file)
    
        
        # Ensure the file pointer is at the beginning before reading
        decrypted_file.seek(0,0)
        decrypted_content = decrypted_file.read()

        # Calculate the hash digest of the file before download
        hash_bfr_download = FileIntegrity.objects.get(file = file_obj).sha256_hash

        response = HttpResponse(decrypted_content, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file_name}.txt"'

        # Calculate the hash digest of the file after download
        hash_after_download = hashlib.sha256(response.content).hexdigest()

        # No two different inputs even with the slightest change have the same hash digest unless modified
        if hash_bfr_download != hash_after_download: # report error if they are not the same
            messages.error(request, "File integrity has been compromised, cannot download this file")
            return redirect('file_app:profile')

        # returns if they are the same
        return response

    except File.DoesNotExist as e:
        messages.error(request, f"File does not exist: {str(e)}")
        return redirect('file_app:profile')
        
