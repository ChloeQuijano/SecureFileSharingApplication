"""
Registration of models for admin page
"""
from django.contrib import admin
from .models import File, FileIntegrity, SharedFile

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """Register File Admin class"""
    list_display = ('file_name', 'owner', 'upload_date', 'is_shared')

@admin.register(FileIntegrity)
class FileIntegrityAdmin(admin.ModelAdmin):
    """Register File Integrity class"""
    list_display = ('file', 'sha256_hash')

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    """Register Shared File Admin"""
    list_display = ('user', 'file', 'permission', 'access_date', 'file_name')
