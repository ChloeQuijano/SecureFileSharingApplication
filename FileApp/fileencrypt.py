from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files.base import ContentFile


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
        encrypted = encrypted_file.read()

        # decrypt the data
        decrypted = f.decrypt(encrypted)

        # rewrite the data in file to decrypted data
        decrypted_file = ContentFile(decrypted)

        # Set the name and content of the file field
        decrypted_file.name = encrypted_file.name
        encrypted_file.save(encrypted_file.name, decrypted_file)

        # Return the modified File object
        return encrypted_file
