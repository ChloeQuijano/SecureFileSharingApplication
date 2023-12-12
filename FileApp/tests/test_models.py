"""
Tests for the models of the FileApp app.
"""
from django.test import TestCase
from django.core.files.base import ContentFile
from django.contrib.auth.models import User  # For user authentication
from FileApp.models import File, FileIntegrity, SharedFile

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

    def test_get_file_size_kb(self):
        """Test getting the file size in KB"""
        self.assertEqual(self.test_file.get_file_size_kb(), 0.02)

    def test_str(self):
        """Test returning the file name"""
        self.assertEqual(self.test_file.__str__(), 'Test file')

class FileIntegrityModelTestClass(TestCase):
    """Test FileIntegrity model"""
    @classmethod
    def setUp(self):
        # user account created
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test file instance
        content = b'Test file content'
        file_content = ContentFile(content, name='test_file.txt')
        test_file = File.objects.create(
            owner=self.user,
            file=file_content,
            file_name='Test file',
            file_size=file_content.size
        )

        # Create a test file integrity instance
        self.test_fileintegrity = FileIntegrity.objects.create(
            file=test_file,
            sha256_hash='Test hash'
        )

    def test_fileintegrity_creation(self):
        """Test that the file integrity instance is created successfully"""
        self.assertEqual(FileIntegrity.objects.count(), 1)

    def test_fileintegrity_update(self):
        """Test updating a field of the file integrity"""
        self.test_fileintegrity.sha256_hash = 'Updated hash'
        self.test_fileintegrity.save()
        self.assertEqual(self.test_fileintegrity.sha256_hash, 'Updated hash')

    def test_fileintegrity_deletion(self):
        """Test deleting the file integrity instance"""
        self.test_fileintegrity.delete()
        self.assertEqual(FileIntegrity.objects.count(), 0)

    def test_str(self):
        """Test returning the file name"""
        self.assertEqual(self.test_fileintegrity.__str__(), 'Test file')

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

    def test_str(self):
        """Test returning the username, filename and permission level"""
        self.assertEqual(self.test_sharedfile.__str__(), 'testuser2 - Test file (edit)')

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
