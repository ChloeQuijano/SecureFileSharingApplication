# Tests

This README contains information on running this test folder and the structure of the test files within in relation to the features of our application.

## Running tests

Be in the root folder of project and run the command below

`py manage.py test`

## Folder Structure

This contains information around the tasks outlined for Assignment 2 and where the test cases are located.

- User Registration and Authentication
    - `test_models.py`
        - UserModelTestClass: tests for user model creation, update and deletion
    - `test_forms.py`
        - RegisterFormTestClass: tests for user registration forms
        - LoginFormTestClass: tests for user login form
    - `test_views.py`
        - ViewsTestClass: tests for opening registration and login pages
        - PostViewsTestClass: tests for inserting user information in sign up and login pages
        - AuthenticatedViewsTestClass: tests for opening profile page upon login of user
    - `test_security.py`
        - TestValidation: test functions for checking valid input data
        - TestUserRegistration: test registration data is valid
- File Upload and Download, File Integrity Check
    - `test_models.py`
        - FileModelTestClass, FileIntegrityModelTestClass: test creation, update, deletion and in built functions for class. Ensures checking of hashing and integrity of objects
    - `test_forms.py`
        - UploadFormTestClass: test Upload file form for uploading file object and inputs
    - `test_views.py`
        - AuthenticatedViewTestClass: tests for opening upload pages. Page requiring login
        - PostViewsTestClass: tests for post request in uploading file. Checks for hashing completion and integrity of type + size of file
        - DownloadFileViewTest: specific tests for view of Download file page. Checking of integrity of file on download
    - `test_security.py`
        - TestFileValidation: tests functions for checking file type and size when uploading
- Sharing Files
    - `test_models.py`
        - SharedFileModelTestClass: test creation, update, deletion and in built functions for class. Ensures checking of hashing and integrity of objects
    - `test_forms.py`
        - ShareFileFormTestClass: test Share file form for sharing of file with users
    - `test_views.py`
        - AuthenticatedViewTestClass: tests for opening share pages. Page requiring login
        - PostViewsTestClass: tests for post request in sharing of file.
    - `test_security.py`
        - TestFileValidation: tests functions for permission of user for sharing
- Test Execution and Reporting
    - `pylint-coverage` folder
        - `README.md`: information for generating reports and folder structure
        - `pylint.txt`: copy of pylint report
        - Screenshots: Running of tests and example of coverage report
