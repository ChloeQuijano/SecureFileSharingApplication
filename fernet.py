"""
To be run separately, generate your own key for Fernet
"""

from cryptography.fernet import Fernet

key = Fernet.generate_key()
key_string = key.decode('utf-8')
print(key_string)