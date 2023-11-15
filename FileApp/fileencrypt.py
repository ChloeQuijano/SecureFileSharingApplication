"""
Class for encrypting the files
"""
import hashlib
from io import BytesIO
from cryptography.fernet import Fernet

class FileEncryptor():
    """
    Class for file ecryption and decryption for upload and retrieval from database
    """
    def __init__(self,key) -> None:
        self.key = key 

    def file_encrypt(self, original_file):
        """
        Takes the InMemoryUploadedFile object and encrypts the data within
        """
        f = Fernet(self.key)

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
        f = Fernet(self.key)

        # open the encrypted file
        encrypted_file.seek(0)
        encrypted = encrypted_file.read()

        # decrypt the data
        decrypted = f.decrypt(encrypted)
        decrypted_instance = BytesIO(decrypted)
        decrypted_instance.seek(0)

        return decrypted_instance

def file_hashing(file_content):
    """
    Calculate hash file content
    """
    hash_obj = hashlib.sha256(file_content).hexdigest()
    return hash_obj
