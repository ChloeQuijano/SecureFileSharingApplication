from django.db import models
from django.contrib.auth.models import User  # For user authentication

class File(models.Model):
    """
    Class for storing file data
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who uploaded the file
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads')
    file_key = models.CharField(max_length=500, default='None')
    encrypted = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, related_name='shared_files', blank=True)
    is_shared = models.BooleanField(default=False)
    file_size = models.PositiveIntegerField()  # File size in bytes
    file_type = models.CharField(max_length=100)  # Type of the file (e.g., text file)

    def get_file_size_kb(self):
        """
        Convert file size in bytes to KB
        """
        return round(self.file_size / (1024), 2)

    def __str__(self):
        """Returns the file name"""
        return self.file_name

class FileIntegrity(models.Model):
    """
    Class for storing file integrity data
    """
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    sha256_hash = models.CharField(max_length=64)

    def __str__(self):
        """Returns the file name"""
        return self.file.file_name

class SharedFile(models.Model):
    """
    Class for shared file data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now=True) # optional
    permission = models.CharField(max_length=50)  # We can use this field to specify the level of access (e.g., read, edit, delete)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        """Returns the username, filename and permission level"""
        return f"{self.user.username} - {self.file.file_name} ({self.permission})"
    class Meta:
        unique_together = ['user', 'file']  # Ensure each user can only share a file with a specific user once
