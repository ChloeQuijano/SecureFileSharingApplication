# SecureFileSharingApplication
SEP300 Group Assignment 1: Secure File Sharing Application

Django application with PostgresSQL database that allows secure file sharing between users

## Run the app
```
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## Assignment Tasks
- User Registration and Authentication:
    - Users should be able to register with a username and password.
    - Implement secure authentication mechanisms to protect user credentials.
- File Upload and Download:
    - Authenticated users should be able to upload files to the server.
    - The uploaded files should be encrypted using symmetric encryption (e.g., AES) to ensure confidentiality.
    - Files should be stored securely on the server, and unauthorized access should be prevented.
    - Users should be able to download their own uploaded files.
- Sharing Files:
    - Implement a secure mechanism for users to share files with specific other users.
    - Only authorized users should be able to access shared files.
- File Integrity Check:
    - Implement a mechanism to ensure file integrity during upload and download using cryptographic hashes (e.g., SHA-256).
    - Detect and handle any modifications to the file during transmission.
- Documentation and Testing:
    - Provide clear documentation for your code, including comments and docstrings.
    - Write comprehensive unit tests to ensure the correctness of your code.

Other Instructions:
- Use Python's built-in libraries for encryption and cryptographic operations.
- Implement the file-sharing application as a command-line interface (CLI) or a web application (using Flask or Django).
- Ensure the application is user-friendly and includes informative error handling.
- Use secure coding practices to prevent common vulnerabilities (e.g., SQL injection, XSS attacks)

## Running tests

Files for test cases are in tests file. To run the tests:

`py manage.py test`

To run coverage report with tests:

`coverage run ./manage.py test FileApp`

This generates a `.coverage` file. To convert the file to an html for viewing, run:

`coverage html`

Running and creating pylint report:

`pylint FileApp > pylint.txt`