# Secure File Sharing Application

Django application with PostgresSQL database that allows secure file sharing between users

## Run the app
```
pip install -r requirements.txt
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## Assignment 1 Tasks
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

## Assignment 2 Tasks
Unit Testing for our Secure File Sharing Application
- User Registration and Authentication (3 marks):
    - Verify that the registration process creates a new user with valid input.
    - Test the authentication process to ensure users can log in successfullywith valid credentials.
    - Check that invalid credentials are rejected during authentication.
- File Upload and Download (4 marks):
    - Test file upload functionality for authenticated users.
    - Ensure files are encrypted using symmetric encryption (e.g., AES)during upload.
    - Confirm that users can download their own uploaded files securely.
    - Verify proper handling of unauthorized access attempts during filedownload.
- Sharing Files (3 marks):
    - Test the secure mechanism for users to share files with specific otherusers.
    - Confirm that only authorized users can access shared files.
    - Verify that unauthorized users are unable to access shared files.
- File Integrity Check (2 marks):
    - Test the mechanism to ensure file integrity during both upload anddownload.
    - Confirm the detection and proper handling of any modifications to thefile during transmission using cryptographic hashes (e.g., SHA-256).
- Test Execution and Reporting (3 marks):
    - Configure Pytest to generate detailed test reports.
    - Ensure that your test reports provide valuable insights into test results,including any failures or errors.
    - Use Pytest's reporting features to identify areas for improvement in yourcode
    - You should be achieving 8/10 on pytest score

Other Instructions
- Ensure your unit tests are well-organized and named appropriately.
- Include a README file that provides clear instructions on how to runthe tests.
- Submit your codebase along with the unit tests
- Stick to secure coding practices to prevent common vulnerabilities.
- Consider both positive and negative test cases for each functionality.
- Pay attention to edge cases and error handling in your tests.
- Make sure your tests can be easily executed and understood by others.

## Running tests

Files for test cases are in tests file. To run the tests:

`py manage.py test`

To run coverage report with tests:

`coverage run ./manage.py test FileApp`

This generates a `.coverage` file. To convert the file to an html for viewing, run:

`coverage html`

Running and creating pylint report:

`pylint FileApp > pylint.txt`

### Other Notes

Creation of admin account to check back-end: `python manage.py createsuperuser`
