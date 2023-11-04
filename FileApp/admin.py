from django.contrib import admin
from .models import File, FileIntegrity, SharedFile
# Register your models here.

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'owner', 'upload_date', 'is_shared')

@admin.register(FileIntegrity)
class FileIntegrityAdmin(admin.ModelAdmin):
    list_display = ('file', 'sha256_hash')

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'permission', 'access_date', 'file_name')
