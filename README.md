# Library management system desktop application developed using PyQt5
A system that maintains record of all the books in the library, Issueing and returning of books,Sending reminders to the clients using whatsapp,Adding new books,Deleting books and updating books in the register.

# Modules required:
1.Pywhatkit

2.Pyautogui

3.Pyqt5

4.mysql connector
# ----------------------------------------------------
# To run the app :
1.change the details in dbdetails.py with your mysql database details

2.Execute main.py

# To find your dbdetails:

* use the command:
* SELECT USER,PASSWORD,HOST FROM MYSQL.USER;

# Future Enhancements:
*Using other SQL servers like SQLlite as Mysql requires the constant functioning of mysql server.
* Sending whatsapp messages automatically when the due date is passed,The current system requires the librarian to clik on a button for Automation
* Sending reminder messages through normal SMS as whatsapp web requires continuous internet connection.
* Directly uploading Excel file option as entering information of each book is time consuming.
* Packaging the whole project as an application so it can be used in any platform.

