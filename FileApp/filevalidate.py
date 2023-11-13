import magic
from .models import SharedFile
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

# max bytes for file type
MAX_SIZE = 3 * (1024 * 1024)   # 3MB

class FileValidation(object):
    """
    File type and size validator, used in file model.
    """
    max_size_message = "Ensure this file size is not greater than %(max_size)s bytes. Your file size is %(size)s bytes."
    file_type_message = "Files of type %(file_type)s are not supported. Allowed extensions are: '%(file_types)s'."

    def __init__(self, max_size=MAX_SIZE,file_types=()):
        self.max_size = max_size
        self.file_types = file_types
    
    def __call__(self, fileObj):
        # checks the max size of the file
        if self.max_size is not None and fileObj.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(fileObj.size),
            }
            raise ValidationError(self.max_size_message, 'max_size', params)

        # checks against the type of the file
        if self.file_types:
            file_type = magic.from_buffer(fileObj.read(), mime=True)
            fileObj.seek(0)

            if file_type not in self.file_types:
                params = {'file_type': file_type, 'file_types': self.file_types }
                raise ValidationError(self.file_type_message, 'file_type', params)
        
        return fileObj



def has_permission(file, user):
    """
    Check if the user is the owner of the file
    """
    if file.owner == user:
        return True

    # Check if the file is shared with the user and has 'edit' permission
    shared_file = SharedFile.objects.filter(file=file, user=user).first()
    return shared_file is not None
