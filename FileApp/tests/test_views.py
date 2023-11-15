"""
Tests for page views
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User  # For user authentication
from django.core.files.base import ContentFile
from django.urls import reverse
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
