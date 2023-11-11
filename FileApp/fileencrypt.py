from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files.base import ContentFile
from .models import File, SharedFile
import hashlib

class FileEncryptor():
    """
    Class for file ecryption and decryption for upload and retrieval from database
    """

    def file_encrypt(self, original_file):
        """
        Takes the InMemoryUploadedFile object and encrypts the data within
        """
        
        f = Fernet(settings.ENCRYPTION_KEY.encode("utf-8"))

        # open the file
        original = original_file.read()
        
        # encrypt data in file
        encrypted_data = f.encrypt(original)

        # rewrite the encrypted data into the file
        # Seek to the beginning of the file-like object to write the encrypted data
        original_file.seek(0)
        original_file.truncate(0)
        original_file.write(encrypted_data)

        # Return the modified file
        return original_file

    def file_decrypt(self, encrypted_file):
        """
        Takes a File object input and decrypts the data within and rewrites it to a new file object for return
        """
        
        f = Fernet(settings.ENCRYPTION_KEY.encode("utf-8"))

        # open the encrypted file
        encrypted = encrypted_file.file.read()

        # decrypt the data
        decrypted = f.decrypt(encrypted)

        if isinstance(encrypted_file, File):
        # create new File instance of decrypted data
            decrypted_instance = File()
            decrypted_instance.owner = encrypted_file.owner
            decrypted_instance.file_name = encrypted_file.file_name
            decrypted_instance.file_size = encrypted_file.file_size
            decrypted_instance.file_type = encrypted_file.file_type

            decrypted_instance.file = ContentFile(decrypted, name=encrypted_file.file_name)

        elif isinstance(encrypted_file, SharedFile):
        # create new SharedFile instance of decrypted data
            decrypted_instance = SharedFile()
            decrypted_instance.user = encrypted_file.user
            decrypted_instance.file_name = encrypted_file.file_name
            decrypted_instance.permission = encrypted_file.permission

            decrypted_instance.file = ContentFile(decrypted, name=encrypted_file.file_name)

        else:
            raise ValueError("Unsupported file type")

        return decrypted_instance


# Calculate hash file content
def file_hashing(file_content):
        hash_obj = hashlib.sha256(file_content)
        return hash_obj






