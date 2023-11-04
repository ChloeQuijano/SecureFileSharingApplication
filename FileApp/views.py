from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

# TODO: Make home page where navigation bar contains sign up / login
def home(request):
    return render(request, "home.html")

# TODO: Register a new user account page
def register(request):
    return render(request, "register.html")

# TODO: Login page for user
def login(request):
    return render(request, "login.html")

# TODO: Logout page for user
def logout(request):
    return render(request, "logout.html")

# TODO: After login, can view the files for the user
def profile(request):
    return render(request, "profile.html")

# TODO: Here you will be able to upload a file for that user
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        #TODO: Handle checking file integrity here and create file object to save after checking
        if form.is_valid():
            # file_instance = File(file=request.FILES["file"])
            # file_instance.save()
            return HttpResponse("Successful upload")
    else:
        form = UploadFileForm()
    return render(request, "upload_file.html", {"form": form})