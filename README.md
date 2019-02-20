REST API web application for library.
-

**To create an example database, please run script EXAMPLE_DATABASE.py - remember to change admin credentials**

Web application contains:

/scan/ section where user check if book exists in database

1) If yes, redirect to book detail
2) If not, user decides if add new book - if user confirm adding, API ask to scan barcode again, add book to database from GOOGLEAPIS and redirect to book detail- possibility to add books by using built-in camera (reading ISBN from barcode) and using googleapis.


