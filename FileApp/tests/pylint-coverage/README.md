# Coverage and Pylint Reports

This readme contains information for creating and viewing coverage report for tests and pylint assessment of codebase. 

## Coverage report

To run coverage report with tests, :

`coverage run ./manage.py test FileApp`

This generates a .coverage file. To convert the files to an html for viewing on the browser, run:

`coverage html`

This creates a htmlcov folder which contains htmls of coverage reports for all files. To start, open the `index.html` file

A photo of the 95% coverage is seen in the screenshot within this folder. We decided to use this library instead of the pylint-cov library due to being built upon the Coverage library.

## Pylint Report

Running and creating pylint report:

`pylint FileApp > pylint.txt`

A copy of the pylint report with a 6.86/10 rating is included in this folder