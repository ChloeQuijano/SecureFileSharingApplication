from django import forms
from django.contrib.auth.models import User
from .models import File
from django.contrib.auth.forms import UserCreationForm
from FileApp.filevalidate import FileValidation

class UploadFileForm(forms.Form):
    """
    Form for uploading file
    """
    title = forms.CharField(max_length=255)
    file = forms.FileField(validators=[FileValidation(file_types=('text/plain',))])

class RegisterForm(UserCreationForm):
    """
    Form for user registration
    """
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    """
    Form for user login
    """
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput) 

class ShareFileForm(forms.Form):
    """
    Form for file sharing
    """
    def __init__(self, request, *args, **kwargs):
        super(ShareFileForm, self).__init__(*args, **kwargs)
        self.request = request  # Set the request attribute

        # Exclude current user
        self.fields['shared_user'].queryset = User.objects.exclude(id = request.user.id)

    shared_user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        empty_label="Select user to share with",
    )
    permission = forms.ChoiceField(
        choices=(
            ('read', 'Read'), # can download, not able to share file
            ('edit', 'Edit'), # can both download and share file
        ),
        initial='read',
        widget=forms.RadioSelect,
    )





