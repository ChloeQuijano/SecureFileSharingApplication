from django import forms
from django.contrib.auth.models import User
from .models import File
from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput) 

class ShareFileForm(forms.Form):
    shared_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Select user to share with",
    )
    permission = forms.ChoiceField(
        choices=(
            ('read', 'Read'),
            ('edit', 'Edit'),
        ),
        initial='read',
        widget=forms.RadioSelect,
    )

    def __init__(self, request, *args, **kwargs):
        super(ShareFileForm, self).__init__(*args, **kwargs)
        self.request = request  # Set the request attribute

    def clean(self):
        cleaned_data = super().clean()
        shared_user = cleaned_data.get('shared_user')
        permission = cleaned_data.get('permission')

        if shared_user and shared_user == self.request.user:
            raise forms.ValidationError("You cannot share a file with yourself.")

        return cleaned_data