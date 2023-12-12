"""
Tests for page views
"""
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User  # For user authentication
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from cryptography.fernet import Fernet
from django.contrib.messages import get_messages
from FileApp.forms import LoginForm, RegisterForm
from FileApp.models import File
from FileApp.views import *

class ViewsTestClass(TestCase):
    """Tests for views without login required"""

    def test_home_loads_properly(self):
        """Check that home loads properly"""
        response = self.client.get(reverse('file_app:home'))
        self.assertEqual(response.status_code, 200)

    def test_register_loads_properly(self):
        """Check that the register page loads properly with form"""
        response = self.client.get(reverse('file_app:register'))
        self.assertEqual(response.status_code, 200)

        # checks that the register page contains the register form
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_login_loads_properly(self):
        """Check that the login page loads properly with form"""
        response = self.client.get(reverse('file_app:login'))
        self.assertEqual(response.status_code, 200)

        # checks that the login page contains the login form
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], LoginForm)

class UnauthenticatedViewsTestClass(TestCase):
    """Tests for views with user not logged in"""

    @classmethod
    def setUp(self):
        """Set up for views"""
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # create test file object
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        self.test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

    def test_profile_loads_properly_unauthenticated_user(self):
        """Check that the profile page loads properly with no user"""
        response = self.client.get(reverse('file_app:profile'))
        self.assertEqual(response.status_code, 302) # redirects to login

    def test_upload_loads_properly_unauthenticated_user(self):
        """Check that the file upload page loads properly with no user"""
        response = self.client.get(reverse('file_app:upload_file'))
        self.assertEqual(response.status_code, 302) #redirects user

    def test_share_loads_properly_unauthenticated_user(self):
        """Check that the file share page loads properly with no logged in user"""
        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) #redirects user

class AuthenticatedViewsTestClass(TestCase):
    """Tests for views with user logged in"""

    @classmethod
    def setUp(self):
        """Set up for views"""

        # create test client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

        # create test file object
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        self.test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

    def test_profile_loads_properly_authenticated_user(self):
        """Check that the profile page loads properly with a logged in user"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('file_app:profile'))
        self.assertEqual(response.status_code, 200)

    def test_upload_loads_properly_authenticated_user(self):
        """Check that the file upload page loads properly with a logged in user"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('file_app:upload_file'))
        self.assertEqual(response.status_code, 200)

        # checks that the upload page contains expected content
        self.assertContains(response, 'Upload a file below')

    def test_share_loads_properly_authenticated_user(self):
        """Check that the file share page loads properly with a logged in user"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # checks that the share file page contains expected content
        self.assertContains(response, 'Share File')

class PostViewsTestClass(TestCase):
    """Tests for post views"""

    @classmethod
    def setUp(self):
        """Set up for views"""
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # create test file object
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        self.test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

    def test_register_post_valid_form(self):
        """Test that the register page posts properly, valid form"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "newpassword123",
            "password2": "newpassword123",
        }
        response = self.client.post(reverse("file_app:register"), data)

        # Check response is successful
        self.assertEqual(response.status_code, 200)

    def test_register_post_invalid_form(self):
        """Test that the register page posts properly, invalid form"""
        data = {
            "username": "newuser",
            "email": "invalidemail",  # Invalid email format
            "password1": "password123",
            "password2": "password456",  # Passwords don't match
        }
        response = self.client.post(reverse("file_app:register"), data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

        # Check if the error message is displayed in the response content
        self.assertContains(response, "Form is invalid. Please check your input.")

    @patch('bcrypt.checkpw', return_value=True)  # Mock the bcrypt.checkpw function
    def test_login_post_valid_form(self, mock_checkpw):
        """Test that the login page posts properly, valid form"""
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(reverse("file_app:login"), data)

        # Check response is successful and user is redirected
        self.assertEqual(response.status_code, 302)

        # Check if the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    @patch('bcrypt.checkpw', return_value=False)  # Mock the bcrypt.checkpw function
    def test_login_post_invalid_form(self, mock_checkpw):
        """Test that the login page posts properly, invalid form"""
        data = {
            "username": "testuser",
            "password": "wrongpassword",  # Wrong password
        }
        response = self.client.post(reverse("file_app:login"), data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

    @patch('bcrypt.checkpw', return_value=False)  # Mock the bcrypt.checkpw function
    def test_login_post_invalid_form2(self, mock_checkpw):
        """Test that the login page posts properly, invalid form"""
        data = {
            "username": "wrongusername",  # Wrong username
            "password": "testpassword",
        }
        response = self.client.post(reverse("file_app:login"), data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

    def test_upload_post_valid_form(self):
        """Test that the upload page posts properly, valid form"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        data = {
            "title": "Test file",
            "file": "Test file content",
        }
        response = self.client.post(reverse("file_app:upload_file"), data)

        # Check that response is successful
        self.assertEqual(response.status_code, 200)

    def test_upload_post_invalid_form(self):
        """Test that the upload page posts properly, invalid form"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        data = {
            "title": "Test file",
            "file": "",  # No file uploaded
        }
        response = self.client.post(reverse("file_app:upload_file"), data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

    def test_upload_post_invalid_form2(self):
        """Test invalid form because file name already exists"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        data = {
            "title": "Test file",
            "file": "Test file content",
        }
        response = self.client.post(reverse("file_app:upload_file"), data)

        # check that the file is not uploaded because file name already exists
        self.assertEqual(response.status_code, 200)

    def test_share_post_valid_form(self):
        """Test that the share page posts properly, valid form"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a test user to share with
        test_user2 = User.objects.create_user(username='testuser2', password='testpassword2')

        data = {
            "shared_user": test_user2.id,
            "permission": "read",
        }
        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.post(url, data)

        # Check response is successful
        self.assertEqual(response.status_code, 200)

    def test_share_post_invalid_form(self):
        """Test that the share page posts properly, invalid form"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a test user to share with
        test_user2 = User.objects.create_user(username='testuser2', password='testpassword2')

        data = {
            "shared_user": test_user2.id,
            "permission": "invalid",  # Invalid permission
        }
        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.post(url, data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

    def test_share_post_invalid_form2(self):
        """Test invalid form because user already has permission"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a test user to share with
        test_user2 = User.objects.create_user(username='testuser2', password='testpassword2')

        data = {
            "shared_user": test_user2.id,
            "permission": "read",
        }
        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.post(url, data)

        # Check valid response after sharing the file
        self.assertEqual(response.status_code, 200)

        # Check if the file is shared
        self.assertTrue(SharedFile.objects.filter(user=test_user2).exists())

        # Share the file again
        response = self.client.post(url, data)

        # Check if the form is not valid and the user is not redirected
        self.assertEqual(response.status_code, 200)

    def test_share_post_invalid_form3(self):
        """Test invalid form because user is the owner of the file"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        data = {
            "shared_user": self.user.id,
            "permission": "read",
        }
        url = reverse('file_app:share_file', args=[self.test_file.id])
        response = self.client.post(url, data)

        # Check that user is not redirected due to invalid form
        self.assertEqual(response.status_code, 200)

class DownloadFileViewTests(TestCase):
    """Tests for download_file view"""

    @classmethod
    def setUp(self):
        """Set up for view tests"""
        key_string = get_fernet_key()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a test file and FileIntegrity record
        self.file_content = b'This is a test file content.'
        self.file_hash = hashlib.sha256(self.file_content).hexdigest()

        # Encrypt the file content
        fernet = Fernet(key_string)
        encrypted_file_content = fernet.encrypt(self.file_content)

        # Create a test file object
        test_file = SimpleUploadedFile(
            name="test_file.txt",
            content=encrypted_file_content,
            content_type="text/plain"
        )

        self.test_uploaded_file = File.objects.create(
            owner=self.user,
            file=test_file,
            file_name="Test file",
            file_size=test_file.size,
        )

        # Create a test file integrity instance
        self.test_fileintegrity = FileIntegrity.objects.create(
            file=self.test_uploaded_file,
            sha256_hash=self.file_hash
        )

    def test_download_file_valid(self):
        """Test that the file can be downloaded successfully"""

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Attempt to download the file
        response = self.client.get(
            reverse("file_app:download_file", args=[self.test_uploaded_file.id])
        )

        # Check that response is successful because message returned does not contain an error message
        messages = list(get_messages(response))
        self.assertNotEqual(len(messages), 1)

    def test_download_file_nonexistent(self):
        """Test that a non-existent file cannot be downloaded"""
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Attempt to download a non-existent file
        response = self.client.get(
            reverse("file_app:download_file", args=[999])
        )

        # Check that file does not exist by function redirecting
        self.assertEqual(response.status_code, 302)
