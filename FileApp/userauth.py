import re
import bcrypt


class Validation:
    """
    Class for validating inputs for user registration
    """
    @staticmethod
    def email_valid(email):
        pattern = r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
        return re.match(pattern, email, re.I)

    @staticmethod
    # At least one upper case, lower case and digit and one special char in "!@#$&/"
    def strong_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$&/*])(?=.*\d).{6,}$"
        return re.match(pattern, password)

    @staticmethod
    def username_valid(name):
        name = name.strip()
        return re.match(r"^[a-zA-Z0-9_]+$", name) and (4 <= len(name) <= 30)


class UserRegistration:
    """
    Class for checking user registration information
    """
    def __init__(self, username, email, password, password2):
        self.username = username
        self.email = email
        self.password = password
        self.password2 = password2

    def is_email_valid(self):
        return Validation.email_valid(self.email)

    def hash_password(self):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(self.password.encode('utf-8'), salt)
        return hashed

    def is_password_strong(self):
        return Validation.strong_password(self.password)

    def are_passwords_matching(self):
        return self.password == self.password2

    def is_username_valid(self):
        return Validation.username_valid(self.username)
