REST API web application for managing a library.
-

**To create an example database, please run script EXAMPLE_DATABASE.py - remember to change admin credentials**

This applications using built_in camera to read barcodes from books(ISBN number) and read NonStaffUser(from ID's barcode)


To register/log in - application is using JWT tokens


Web application contains:


-Possibility to scan barcodes to check if book exists in Library's database and then add it to Library's database, if not, StaffUser can add book from GoogleAPIS books using this barcode

-Possibility to add NonStaffUser, who can borrow books with borrow date and returning date. If NonStaffUser exceedes returning date then user must pay fee depends on exceeded days

-Possibility to check User Borrowing book history






