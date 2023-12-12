"""
Test Validation and Registration security classes
"""
from django.test import TestCase, Client
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User  # For user authentication
from FileApp.filevalidate import FileValidation, has_permission
from FileApp.models import File
from FileApp.userauth import Validation, UserRegistration

class TestValidation(TestCase):
    """Test Validation class"""
    def test_email_valid(self):
        """Test that email is valid"""
        test_email = "testemail@example.com"
        email = Validation.email_valid(test_email)
        self.assertTrue(email)

    def test_email_invalid(self):
        """Test that email is invalid by not having an @ symbol"""
        test_email = "testemail"
        email = Validation.email_valid(test_email)
        self.assertFalse(email)

    def test_strong_password(self):
        """Test that password is strong"""
        test_password = "TestPassword123!"
        password = Validation.strong_password(test_password)
        self.assertTrue(password)

    def test_strong_password_invalid(self):
        """Test that password is invalid by not having a special character"""
        test_password = "testpassword"
        password = Validation.strong_password(test_password)
        self.assertFalse(password)

    def test_username_valid(self):
        """Test that username is valid"""
        test_username = "testusername"
        username = Validation.username_valid(test_username)
        self.assertTrue(username)

    def test_username_invalid(self):
        """Test that username is invalid by having a space"""
        test_username = "test username"
        username = Validation.username_valid(test_username)
        self.assertFalse(username)

    def test_username_invalid2(self):
        """Test that username is invalid by being too long"""
        test_username = "testusername12345678901234567890"
        username = Validation.username_valid(test_username)
        self.assertFalse(username)

class TestUserRegistration(TestCase):
    """Test User Registration class"""
    def test_userregistration_valid(self):
        """Test that user registration is valid"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        user = UserRegistration(test_username, test_email, test_password, test_password)
        # Check that the email is valid
        self.assertTrue(user.is_email_valid())

    def test_userregistration_invalid(self):
        """Test that user registration is invalid by not having an @ symbol in the email"""
        test_username = "testusername"
        test_email = "testexample.com"

        # Create a user registration object
        user = UserRegistration(test_username, test_email, test_email, test_email)
        # Check that the email is invalid because it does not have an @ symbol
        self.assertFalse(user.is_email_valid())

    def test_hash_password(self):
        """Test that password is hashed"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the password is hashed and not the same
        hashed = test_user.hash_password()
        self.assertNotEqual(hashed, test_password)

    def test_password_strong(self):
        """Test that password is strong"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the password is strong
        self.assertTrue(test_user.is_password_strong())

    def test_password_strong_invalid(self):
        """Test that password is invalid by not having a special character"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "testpassword"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the password is not strong
        self.assertFalse(test_user.is_password_strong())

    def test_passwords_matching(self):
        """Test that passwords match"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the passwords match
        self.assertTrue(test_user.are_passwords_matching())

    def test_passwords_matching_invalid(self):
        """Test that passwords do not match"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"
        test_password2 = "TestPassword123"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password2)

        # Check that the passwords do not match
        self.assertFalse(test_user.are_passwords_matching())

    def test_username_valid(self):
        """Test that username is valid"""
        test_username = "testusername"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the username is valid
        self.assertTrue(test_user.is_username_valid())

    def test_username_invalid(self):
        """Test that username is invalid by having a space"""
        test_username = "test username"
        test_email = "test@example.com"
        test_password = "TestPassword123!"

        # Create a user registration object
        test_user = UserRegistration(test_username, test_email, test_password, test_password)

        # Check that the username is invalid
        self.assertFalse(test_user.is_username_valid())

class TestFileValidation(TestCase):
    """Test File Validation class"""
    @classmethod
    def setUp(self):
        """Create a test file validation object and user"""
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

        test_file_type = "text/plain"
        test_max_size = 3 * (1024 * 1024) # 3MB
        self.validator = FileValidation(test_max_size, file_types=test_file_type)

    def test_file_size_valid(self):
        """Test that file size is valid"""
        # create a test file object
        content = b'Test file content'
        test_file = ContentFile(content, name='test_file.txt')

        # Check that the file size is valid
        self.assertTrue(self.validator(test_file))

    def test_file_size_invalid(self):
        """Test that file size is invalid by being too large"""
        # create a test file object
        content = b'Test file content' * 1000000
        test_file = ContentFile(content, name='test_file.txt')

        # Check that the file size is invalid through a ValidationError
        with self.assertRaises(ValidationError):
            self.validator(test_file)

    def test_file_type_valid(self):
        """Test that file type is valid"""
        # create a test file object
        content = b'Test file content'
        test_file = ContentFile(content, name='test_file.txt')

        # Check that the file type is valid
        self.assertTrue(self.validator(test_file))

    def test_has_permission_valid(self):
        """Test that user has permission"""
        # create a test file object
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

        # Check that the user has permission
        self.assertTrue(has_permission(test_file, self.user))
