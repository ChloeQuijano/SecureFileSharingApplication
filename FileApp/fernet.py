"""
Used for each file integrity 
"""

from cryptography.fernet import Fernet

def get_fernet_key():
    """Generates a key and returned"""
    key = Fernet.generate_key()
    key_string = key.decode('utf-8')
    return key_string
