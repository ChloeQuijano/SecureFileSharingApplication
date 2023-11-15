from unittest.mock import patch
from django.test import TestCase, Client
from django.core.files.base import ContentFile
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User  # For user authentication
from FileApp.forms import LoginForm, RegisterForm, ShareFileForm, UploadFileForm
from FileApp.models import File
from FileApp.views import *

class UploadFormTestClass(TestCase):
    """Tests for Upload File form"""

    @classmethod
    def setUp(self):
        """Set up user and test file"""
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

        # Create a SimpleUploadedFile with the desired file content
        file_content = b'Test file content'
        self.test_uploaded_file = SimpleUploadedFile("test_file.txt", file_content)

    def test_uploadform_valid_data(self):
        """Test uploading file with valid inputs through POST request"""
        # log in user
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('file_app:upload_file'), {'title': 'Test Title', 'file': self.test_uploaded_file})

        # Check that the response is a redirect to profile page
        self.assertEqual(response.status_code, 302)

    def test_uploadform_missing_title(self):
        """Test the upload file form with missing title"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        form_data = {'file': self.test_uploaded_file}
        form = UploadFileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_uploadform_invalid_file(self):
        """Test the upload file form with an invalid file type"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        content = b'Test file content'
        file_content = ContentFile(content, name='test.jpg')
        test_invalid_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

        form_data = {'title': 'Test Title', 'file': test_invalid_file}
        form = UploadFileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('file', form.errors)
    
    def test_empty_form(self):
        """Test the upload file form with no data"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        # Test the form with no data
        form = UploadFileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('file', form.errors)

class RegisterFormTestClass(TestCase):
    """Tests for user registration form"""

    def test_valid_data(self):
        """Test the form with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_passwords_not_matching(self):
        """Test the form with non-matching passwords"""
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_existing_username(self):
        """Test the form with an existing username"""
        User.objects.create_user(username='existinguser', password='password123')
        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_existing_email(self):
        """Test the form with an existing email"""
        User.objects.create_user(
            username='newuser',
            email='existinguser@example.com',
            password='password123'
        )
        form_data = {
            'username': 'newuser',
            'email': 'existinguser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_empty_form(self):
        """Test the form with no data"""
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

class LoginFormTestClass(TestCase):
    """Tests for login form"""

    @classmethod
    def setUp(self):
        """Create a test user"""
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_valid_data(self):
        """Test the form with valid data"""
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        """Test the form with a missing 'username' field"""
        form_data = {'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_missing_password(self):
        """Test the form with a missing 'password' field"""
        form_data = {'username': 'testuser'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    @patch('bcrypt.checkpw', return_value=False)  # Mock the bcrypt.checkpw function
    def test_invalid_credentials(self, mock_checkpw):
        """Test logging in with invalid credentials through POST request"""
        response = self.client.post(reverse('file_app:login'), {
            'username': 'testuser',
            'password': 'invalidpassword'
        })
        
        # Check that the response is not a redirect
        self.assertEqual(response.status_code, 200)
        
        # Check that the error message is present
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password")

    def test_empty_form(self):
        """Test the form with no data"""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class ShareFileFormTestClass(TestCase):
    """Tests for sharing file form"""

    @classmethod
    def setUp(self):
        """Create a test user"""
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_form_initialization(self):
        """Test form initialization with a request and without errors"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        form = ShareFileForm(request=self.test_user)

        # Check that the queryset excludes the current user
        expected_queryset = User.objects.exclude(id=self.test_user.id)
        self.assertQuerysetEqual(
            form.fields['shared_user'].queryset,
            expected_queryset, transform=lambda x: x
        )

        self.assertTrue(isinstance(
            form.fields['shared_user'].queryset,
            type(User.objects.exclude(id=self.test_user.id))
        ))
        self.assertEqual(form.fields['permission'].initial, 'read')

    def test_valid_data(self):
        """Tests the shared file form with valid inputs"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        # Test the form with valid data
        shared_user = User.objects.create_user(
            username='shareduser',
            password='sharedpassword'
        )
        form_data = {'shared_user': shared_user.id, 'permission': 'edit'}
        form = ShareFileForm(request=self.test_user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_shared_user(self):
        """Test missing shared user in share file form"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        # Test the form with a missing 'shared_user' field
        form_data = {'permission': 'edit'}
        form = ShareFileForm(request=self.test_user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shared_user', form.errors)

    def test_missing_permission(self):
        """Test missing permission input for share file form"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        # Test the form with a missing 'permission' field
        shared_user = User.objects.create_user(username='shareduser', password='sharedpassword')
        form_data = {'shared_user': shared_user.id}
        form = ShareFileForm(request=self.test_user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('permission', form.errors)

    def test_empty_form(self):
        """Tests an empty share file form"""
        # log in user
        self.client.login(username='testuser', password='testpassword')

        # Test the form with no data
        form = ShareFileForm(request=self.test_user, data={})
        self.assertFalse(form.is_valid())
        self.assertIn('shared_user', form.errors)
        self.assertIn('permission', form.errors)