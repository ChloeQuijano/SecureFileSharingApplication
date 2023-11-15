from django.test import TestCase
from django.core.files.base import ContentFile
from django.contrib.auth.models import User  # For user authentication
from FileApp.models import File, SharedFile

class FileModelTestClass(TestCase):
    """Test File model"""
    @classmethod
    def setUp(self):
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test file instance
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        self.test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

    def test_file_creation(self):
        """Test that the file instance is created successfully"""
        self.assertEqual(File.objects.count(), 1)

    def test_file_update(self):
        """Test updating a field of the file"""
        self.test_file.name = 'Updated File'
        self.test_file.save()
        self.assertEqual(self.test_file.name, 'Updated File')

    def test_file_deletion(self):
        """Test deleting the file instance"""
        self.test_file.delete()
        self.assertEqual(File.objects.count(), 0)

class SharedFileModelTestClass(TestCase):
    """Test SharedFile model"""
    @classmethod
    def setUp(self):
        # user account created
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # user to share with account created
        self.user_sharedto = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )

        # Create a test shared file instance
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

        self.test_sharedfile = SharedFile.objects.create(
            user=self.user_sharedto,
            file=test_file,
            permission='edit',
            file_name=test_file.file_name
        )

    def test_sharedfile_creation(self):
        """Test that the shared file instance is created successfully"""
        self.assertEqual(SharedFile.objects.count(), 1)

    def test_sharedfile_update(self):
        """Test updating a shared field of the file"""
        self.test_sharedfile.file_name = 'Updated File'
        self.test_sharedfile.save()
        self.assertEqual(self.test_sharedfile.file_name, 'Updated File')

    def test_sharedfile_deletion(self):
        """Test deleting the shared file instance"""
        self.test_sharedfile.delete()
        self.assertEqual(SharedFile.objects.count(), 0)

class UserModelTestClass(TestCase):
    """Test User model"""
    @classmethod
    def setUp(self):
        """create a test user instance"""
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_user_creation(self):
        """Test that the user instance is created successfully"""
        self.assertEqual(User.objects.count(), 1)

    def test_user_update(self):
        """Test updating a field of the user"""
        self.test_user.username = 'updateduser'
        self.test_user.save()
        self.assertEqual(self.test_user.username, 'updateduser')

    def test_user_deletion(self):
        """Test deleting the user instance"""
        self.test_user.delete()
        self.assertEqual(User.objects.count(), 0)
