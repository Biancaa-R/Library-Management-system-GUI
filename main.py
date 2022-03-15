#importing necessary modules
import pywhatkit, datetime, time
import dbdetails, db
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import mysql.connector

#creating database and new table in mysql 
dbuser, dbpass = dbdetails.execute()
db.exec(dbuser,dbpass)

#Connecting to database
mydb = mysql.connector.connect(
    host = "localhost",
    user = dbuser,            
    password = dbpass,
    database = "Library"
    )
         
cursor = mydb.cursor()
cursor = mydb.cursor(buffered=True)

#creating the register class, displays all books and their details
#user can search for records based on any category
class register(QDialog):
    def __init__(self):
        super(register, self).__init__()
        loadUi("table.ui",self)
        self.homeButton.clicked.connect(self.gotodash)
        self.pushButton.clicked.connect(self.gototype)
        self.logout.clicked.connect(self.gotologout)
        self.searchfield.setPlaceholderText("Search..")
        self.searchfield.textChanged.connect(self.gotosearch)
        self.searchButton.clicked.connect(self.gotosearch)
        cursor.execute("SELECT * FROM Register")
        result=cursor.fetchall()
        self.registertable.setColumnCount(len(result[0]))
        self.registertable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.registertable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def gotosearch(self):
        searchvalue = self.searchfield.text()
        category = self.categoryBox.currentText()
        cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(category, searchvalue))
        result=cursor.fetchall()
        if result:
            self.label.setText("")
            self.registertable.setColumnCount(len(result[0]))
            self.registertable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.registertable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            self.label.setText("No such record found.")
            cursor.execute("SELECT * FROM Register")
            result=cursor.fetchall()
            self.registertable.setColumnCount(len(result[0]))
            self.registertable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.registertable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def gototype(self):
        typesearch=TypeSearch()
        widget.addWidget(typesearch)
        widget.setCurrentWidget(typesearch)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

#creating typesearch class, to search for records by typing
class TypeSearch(QDialog):
    def __init__(self):
        super(TypeSearch, self).__init__()
        loadUi("searchtype1.ui", self)
        self.tableWidget.setColumnWidth(0,25)
        self.tableWidget.setColumnWidth(1,200)
        self.tableWidget.setColumnWidth(5,150)
        self.searchButton.clicked.connect(self.gotosearching)
        self.backButton.clicked.connect(self.gotoprevious)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        self.loaddata()

    def gotoprevious(self):
        reg=register()
        widget.addWidget(reg)
        widget.setCurrentWidget(reg)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard) 

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

    def loaddata(self):
        cursor.execute("SELECT * FROM REGISTER")
        data=cursor.fetchall()
        row=0
        self.tableWidget.setRowCount(len(data))
        for i in data:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i[4])))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i[5])))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i[6])))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(i[7])))
            self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(i[8])))
            self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(i[9])))
            
            row=row+1
        
    def gotosearching(self):
        global searchvalue, category
        searchvalue = self.searchfield.text()
        category=self.categoryfield.text()
        try:
            cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(category, searchvalue))
            data = cursor.fetchall()
            if data:
                search= SearchPage() 
                widget.insertWidget(2, search)
                widget.setCurrentIndex(2)
            else:
                self.confirm.setText("No record exists.")
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong. Please try again after checking all the values.")
      
class SearchPage(QDialog):
    def __init__(self):
        super(SearchPage,self).__init__()
        loadUi("searchtype2.ui",self)
        self.backButton.clicked.connect(self.gototype)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        try:
            cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(category, searchvalue))
            value=cursor.fetchall()
            row=0
            self.tableWidget.setRowCount(len(value))
            for r in value:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(r[0])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(r[1])))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(r[2])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(r[3])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(r[4])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(r[5])))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(r[6])))
                self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(r[7])))
                self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(r[8])))
                self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(r[9])))
                row=row+1
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong. Please try again after checking your values.")

    def gototype(self):
        typesearch=TypeSearch()
        widget.addWidget(typesearch)
        widget.setCurrentWidget(typesearch)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)        

#creating issuebooks class, can be used to both issue books or mark them returned
class IssueBooks(QDialog):
    def __init__(self):
        super(IssueBooks, self).__init__()
        loadUi("issueBooks.ui", self)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        self.issuebutton.clicked.connect(self.issueprocess)
        self.returnbutton.clicked.connect(self.returnprocess)
        self.reminderButton.clicked.connect(self.reminderprocess)
        self.tableButton.clicked.connect(self.gotoissuetable)
        self.portalButton.clicked.connect(self.gotoremportal)
        try:
            cursor.execute("SELECT * FROM IssueDetails ORDER BY Date_issued DESC")
            result = cursor.fetchall()
            if result:
                self.registertable.setColumnCount(len(result[0]))
                self.registertable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.registertable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong.")
    #defining the process to issue books
    def issueprocess(self):
        global Rollno
        global Book
        global Author
        global Spno
        Spno = self.spnofield.text()
        Book = self.bookfield.text()
        Author = self.authorfield.text()
        Rollno = self.rollnofield.text()
        if Spno:
            cursor.execute("SELECT * FROM Register WHERE Sp_no = {}".format(Spno, ))
            data = cursor.fetchall()
                            
            def new():
                global Rollno
                global Book
                global Author
                global Spno
                #checking for details, retrieving them if not already specified
                if not Author:
                    cursor.execute("SELECT Author_Name FROM Register WHERE Sp_no = {}".format(Spno, ))
                    a = cursor.fetchone()
                    if a != "NULL":
                        Author = ""
                        for i in a:
                            Author += i
                if not Book:
                    cursor.execute("SELECT Book_Title FROM Register WHERE Sp_no = {}".format(Spno, ))
                    a = cursor.fetchone()
                    if a != "NULL":
                        Book = ""
                        for i in a:
                            Book += i
                if Rollno:
                    try:
                        y= datetime.datetime.now()+datetime.timedelta(days=7)
                        y=str(y)
                        cursor.execute('INSERT INTO IssueDetails(Sp_no, Book_Title, Author_Name, Roll_no,due)\
                            VALUES ({}, "{}", "{}", {},"{}")'.format(Spno, Book, Author, Rollno,y))
                        mydb.commit()
                        self.confirm.setText("Book issued!")
                    except mysql.connector.Error as Err:
                        self.confirm.setText("Something went wrong. Please check the values and try again.")
                        print(Err)
                else:
                    self.confirm.setText("Something went wrong. Please check the values and try again.")


                cursor.execute("SELECT * FROM IssueDetails ORDER BY Date_issued DESC")
                result = cursor.fetchall()
                if result:
                    self.registertable.setRowCount(len(result))
                    self.registertable.setColumnCount(len(result[0]))
                    self.registertable.setRowCount(0)
                    for row_number, row_data in enumerate(result):
                        self.registertable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                        #print(column_number)
                            self.registertable.setItem(
                                row_number, column_number, QTableWidgetItem(str(data)))
                else:
                    pass
            if data:
                cursor.execute("SELECT Status FROM IssueDetails WHERE Sp_no = {} ORDER BY Date_issued DESC LIMIT 1".format(Spno, ))
                a = cursor.fetchone()
                if a:
                    status = ""
                    for i in a:
                        status += i

                    else:
                        pass
                    
                    if str(status) == "Borrowed":
                        self.confirm.setText("Book is already borrowed. Mark returned and try again.")
                    else:
                        new()

                else:
                    new()

            else:
                self.confirm.setText("Book not found")
        else:
            self.confirm.setText("Something went wrong. Please check the values and try again.")
    #defining the process of returning book
    def returnprocess(self):
        Spno = self.returnedspnofield.text()
        if Spno:
            cursor.execute("SELECT * FROM IssueDetails WHERE Sp_no = {}".format(Spno, ))
            data = cursor.fetchall()
            if data:
                try:
                    cursor.execute("""UPDATE IssueDetails SET Status = 'Returned' 
                    WHERE Sp_no = {} ORDER BY Date_issued DESC LIMIT 1""".format(Spno,))
                    mydb.commit()
                    self.confirm.setText("Book marked returned!")
                except mysql.connector.Error as Err:
                    self.confirm.setText("Something went wrong. Please try again.")
                    print(Err)
            else:
                self.confirm.setText("Book doesn't exist or hasn't been issued")

            cursor.execute("SELECT * FROM IssueDetails ORDER BY Date_issued DESC")
            result = cursor.fetchall()
            if result:
                self.registertable.setColumnCount(len(result[0]))
                self.registertable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.registertable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            else:
                pass
        else:
            self.confirm.setText("Please enter a value.")

    def reminderprocess(self):
        Rollno = self.rollnofield.text()
        if Rollno:  
            cursor.execute("SELECT STATUS FROM IssueDetails WHERE Roll_no = {}".format(Rollno,))
            data = cursor.fetchall()
            if data:
                L = []
                for i in data:
                    for j in i:
                        L.append(j)
                if "Borrowed" in L:
                    cursor.execute("SELECT PHONE FROM CLIENTINFO WHERE ROLL_NO= {}".format(Rollno))
                    result = cursor.fetchall()
                    if not result:
                        self.confirm.setText("The user does not exist.")
                    else:
                        cursor.execute("SELECT NAME FROM CLIENTINFO WHERE ROLL_NO= {}".format(Rollno))
                        name = cursor.fetchone()[0]
                        cursor.execute("SELECT DATE_ISSUED FROM ISSUEDETAILS WHERE ROLL_NO= {} AND STATUS = 'Borrowed'".format(Rollno))
                        date = cursor.fetchone()[0]
                        name = str(name)
                        date = str(date)
                        date = date[:10]

                        for i in result:
                            for j in i:
                                j = str(j)
                        pywhatkit.sendwhatmsg_instantly("+91"+j, "Hello, this is the Librarian. "+name+", please return the book soon. The book was borrowed on "+date+".", tab_close=True)
                        self.confirm.setText("Message successfully sent!")
                else:
                    self.confirm.setText("The user has returned all books.")
            else:
                self.confirm.setText("The user does not exist or hasn't borrowed anything yet.")
        else:
            self.confirm.setText("Enter the roll number to send reminder for.")       
    
    def gotoissuetable(self):
        issue = IssueTable()
        widget.addWidget(issue)
        widget.setCurrentWidget(issue)

    def gotoremportal(self):
        rempor = ReminderPortal()
        widget.addWidget(rempor)
        widget.setCurrentWidget(rempor)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

#creating the issuetableclass, displays all past issues and returns of books
class IssueTable(QDialog):
    def __init__(self):
        super(IssueTable, self).__init__()
        loadUi("issuetable.ui",self)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        self.searchfield.setPlaceholderText("Search..")
        self.searchfield.textChanged.connect(self.gotosearch)
        self.searchButton.clicked.connect(self.gotosearch)
        cursor.execute("SELECT * FROM IssueDetails")
        result=cursor.fetchall()
        self.registertable.setColumnCount(len(result[0]))
        self.registertable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.registertable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data))) 

    def gotosearch(self):
        searchvalue1 = self.searchfield.text()
        category1 = self.categoryBox.currentText()
        cursor.execute("SELECT * FROM IssueDetails WHERE {} LIKE '%{}%'".format(category1, searchvalue1))
        result=cursor.fetchall()
        if result:
            self.label.setText("")
            self.registertable.setColumnCount(len(result[0]))
            self.registertable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.registertable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            self.label.setText("No such record found.")
            cursor.execute("SELECT * FROM IssueDetails")
            result=cursor.fetchall()
            self.registertable.setColumnCount(len(result[0]))
            self.registertable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.registertable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)   

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

#the reminder portal, used to send reminders to users when they have to return a book
class ReminderPortal(QDialog):
    def __init__(self):
        super(ReminderPortal, self).__init__()
        loadUi("reminderportal.ui", self)
        self.submitButton.clicked.connect(self.reminderprocess)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        self.issuedetails.clicked.connect(self.gotoissuedetails)

    def reminderprocess(self):
        Rollno = self.rollnofield.text()
        if Rollno:  
            cursor.execute("SELECT STATUS FROM IssueDetails WHERE Roll_no = {}".format(Rollno,))
            data = cursor.fetchall()
            if data:
                L = []
                for i in data:
                    for j in i:
                        L.append(j)
                if "Borrowed" not in L:
                    self.confirm.setText("The user has returned all books.")
                else:    
                    message = self.messagefield.text()
                    if len(message) == 0:
                        message = "Please return your book soon. Thankyou!"
                    cursor.execute("SELECT PHONE FROM CLIENTINFO WHERE ROLL_NO= {}".format(Rollno))
                    result = cursor.fetchall()
                    if not result:
                        self.confirm.setText("The user does not exist.")
                    else:
                        cursor.execute("SELECT NAME FROM CLIENTINFO WHERE ROLL_NO= {}".format(Rollno))
                        name = cursor.fetchone()[0]
                        cursor.execute("SELECT DATE_ISSUED FROM ISSUEDETAILS WHERE ROLL_NO= {}".format(Rollno))
                        date = cursor.fetchone()[0]
                        name = str(name)
                        date = str(date)
                        date = date[:10]
                        for i in result:
                            for j in i:
                                j = str(j)
                        pywhatkit.sendwhatmsg_instantly("+91"+j, "Hello, this is the Librarian. "+name+", "+message+". The book was borrowed on "+date+".", tab_close=True)
                        time.sleep(2)
                        self.confirm.setText("Message successfully sent!")
            else:
                self.confirm.setText("The user does not exist or hasn't borrowed anything yet.")
        else:
            self.confirm.setText("Enter the roll number to send reminder for.")

    def gotoissuedetails(self):
        issuebooks = IssueBooks()
        widget.addWidget(issuebooks)
        widget.setCurrentWidget(issuebooks)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

#creating updatemenu class, a menu to navigate to different update processes
#which are add, delete and update
class UpdateMenu(QDialog):
    def __init__(self):
        super(UpdateMenu, self).__init__()
        loadUi("updateMenu.ui", self)
        self.addbooksbutton.clicked.connect(self.gotoaddbooks)
        self.delbooksbutton.clicked.connect(self.gotodelbooks)
        self.updatebutton.clicked.connect(self.gotoupdatebooks)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotoaddbooks(self):
        addbooks = AddBooks()
        widget.addWidget(addbooks)
        widget.setCurrentWidget(addbooks)

    def gotodelbooks(self):
        delbooks = DeleteBooks()
        widget.addWidget(delbooks)
        widget.setCurrentWidget(delbooks)

    def gotoupdatebooks(self):
        updatebooks1 = UpdateBooks1()
        widget.addWidget(updatebooks1)
        widget.setCurrentWidget(updatebooks1)

#creating addbooks class, one can add new records through here
class AddBooks(QDialog):
    def __init__(self):
        super(AddBooks, self).__init__()
        loadUi("addBooks.ui",self)
        self.addButton.clicked.connect(self.takevalue)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        
    def takevalue(self):
        Spno = self.spnofield.text()
        Name = self.namefield.text()
        Author = self.authorfield.text()
        Publisher = self.publisherfield.text()
        Class = self.classfield.text()
        Year = self.yearfield.text()
        Edition = self.editionfield.text()
        Subject = self.subjectfield.text()
        Category = self.categoryfield.text()
        Cost = self.costfield.text()

        if len(Spno)!=0:
            cursor.execute("SELECT * FROM Register WHERE Sp_no = {}".format(Spno, ))
            data = cursor.fetchall()
            if data:
                self.confirm.setText("Record with same specimen number already exists.")
            else:
                charvalues = [Author, Edition, Subject, Category]
                for i in charvalues:
                    if len(i) == 0:
                        i = ''
                    else:
                        pass
                query = """INSERT INTO REGISTER (Sp_no, Book_Title, Author_Name, Publisher, Class, Year_of_Publication, Edition, Subject, Category, Cost)
                    VALUES ({}, "{}", "{}", "{}", {}, {}, "{}", "{}", "{}", {})""".format(Spno, Name, Author, Publisher, Class, Year, Edition, Subject, Category, Cost)
                if not Class:
                    query = """INSERT INTO REGISTER (Sp_no, Book_Title, Author_Name, Publisher, Class, Year_of_Publication, Edition, Subject, Category, Cost)
                    VALUES ({}, "{}", "{}", "{}", NULL, {}, "{}", "{}", "{}", {})""".format(Spno, Name, Author, Publisher, Year, Edition, Subject, Category, Cost)
                if not Year:
                    query = """INSERT INTO REGISTER (Sp_no, Book_Title, Author_Name, Publisher, Class, Year_of_Publication, Edition, Subject, Category, Cost)
                    VALUES ({}, "{}", "{}", "{}", {}, NULL, "{}", "{}", "{}", {})""".format(Spno, Name, Author, Publisher, Class, Edition, Subject, Category, Cost)
                if not Class and not Year:
                    query = """INSERT INTO REGISTER (Sp_no, Book_Title, Author_Name, Publisher, Class, Year_of_Publication, Edition, Subject, Category, Cost)
                    VALUES ({}, "{}", "{}", "{}", NULL, NULL, "{}", "{}", "{}", {})""".format(Spno, Name, Author, Publisher, Edition, Subject, Category, Cost)
                try:
                    cursor.execute(query)
                    self.confirm.setText("Book added successfully!")
                except mysql.connector.Error as Err:
                    self.confirm.setText("Something went wrong. Try again after checking all values.")
                mydb.commit()
                
        elif len(Spno) == 0:
            self.confirm.setText("Something went wrong. Try again after checking all values.")
        
    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard) 

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

#creating deletebooks class, one can delete records through here
class DeleteBooks(QDialog):
    def __init__(self):
        super(DeleteBooks, self).__init__()
        loadUi("deleteBooks.ui",self)
        self.homeButton.clicked.connect(self.gotodash)
        self.searchButton.clicked.connect(self.gotosearch)
        self.logout.clicked.connect(self.gotologout)
        self.confirmbutton.clicked.connect(self.gotosearchfirst)

    def gotosearchfirst(self):
        self.confirm.setText("First search for the book to be deleted.")

    def gotosearch(self):
        global searchvalue, category
        searchvalue = self.searchfield.text()
        category = self.categoryBox.currentText()
        if searchvalue:
            cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(category, searchvalue))
            result=cursor.fetchall()
            if not result:
                self.confirm.setText("No record found.")
            else:
                self.confirm.setText("")
                self.registertable.setColumnCount(len(result[0]))
                self.registertable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.registertable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                if len(result)>1:
                    confirmbox = confirmBox()
                    if confirmbox.exec_():
                        self.confirm.setText("Click on proceed.")
                        self.confirmbutton.clicked.connect(self.multidelete)
                    else:
                        choose = Choose()
                        if choose.exec_():
                            global spno
                            spno = choose.spnofield.text()
                            self.confirm.setText("Click on proceed.")
                            self.confirmbutton.clicked.connect(self.choosedelete)
                        else:
                            pass
                        #self.confirm.setText("Please search using another value such that only 1 required record is visible.")
                else:
                    self.confirm.setText("Click on proceed.")
                    self.confirmbutton.clicked.connect(self.singledelete)
        else:
            self.confirm.setText("Please enter a value.")

    def choosedelete(self):
        try:
            cursor.execute("DELETE FROM REGISTER WHERE Sp_No = '{}'".format(spno))
            mydb.commit()
            self.confirm.setText("Book deleted successfully")
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong. Please try again.")

    def singledelete(self):
        try:
            cursor.execute("DELETE FROM REGISTER WHERE {} = '{}'".format(category, searchvalue))
            mydb.commit()
            self.confirm.setText("Book deleted successfully")
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong. Please try again.")

    def multidelete(self):
        try:
            cursor.execute("DELETE FROM REGISTER WHERE {} LIKE '%{}%'".format(category, searchvalue))
            mydb.commit()
            self.confirm.setText("Books deleted successfully")
        except mysql.connector.Error:
            self.confirm.setText("Something went wrong. Please try again.")

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

class confirmBox(QDialog):
    def __init__(self):
        super(confirmBox, self).__init__()
        loadUi("confirmbox.ui", self)
        self.okButton.clicked.connect(self.gotook)
        self.cancelButton.clicked.connect(self.gotocancel)

    def gotook(self):
        self.accept()
        
    def gotocancel(self):
        self.reject()

class Choose(QDialog):
    def __init__(self):
        super(Choose, self).__init__()
        loadUi("choose.ui", self)
        self.okButton.clicked.connect(self.gotook)
        self.cancelButton.clicked.connect(self.gotocancel)

    def gotook(self):
        self.accept()

    def gotocancel(self):
        self.reject()

#creating updatebooks class, one can update records through here
class UpdateBooks1(QDialog):
    def __init__(self):
        super(UpdateBooks1, self).__init__()
        loadUi("updateBooks1.ui", self)
        self.homeButton.clicked.connect(self.gotodash)
        self.searchButton.clicked.connect(self.gotosearch)
        self.logout.clicked.connect(self.gotologout)
        self.confirmbutton.clicked.connect(self.searchfirst)

    def searchfirst(self):
        self.confirm.setText("First search for the book to be updated.")        

#searching for a record to update
    def gotosearch(self):
        global updatesearchvalue, updatecategory
        updatesearchvalue = self.searchfield.text()
        updatecategory = self.categoryBox.currentText()
        if updatesearchvalue:
            cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(updatecategory, updatesearchvalue))
            result=cursor.fetchall()
            if result:
                self.confirm.setText("")
                self.registertable.setColumnCount(len(result[0]))
                self.registertable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.registertable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                #checking for similar records
                if len(result)>1:
                    choose = Choose()
                    if choose.exec_():
                        updatesearchvalue = choose.spnofield.text()
                        self.confirm.setText("Click on proceed.")
                        self.confirmbutton.clicked.connect(self.updateBooks)
                    else:
                        self.confirm.setText("Enter a value.")                    
                else:
                    self.confirm.setText("Click on proceed.")
                    self.confirmbutton.clicked.connect(self.updateBooks)
            else:
                self.confirm.setText("No record found.")
        else:
            self.confirm.setText("Something went wrong. Please try again after checking all values.")
            

    def updateBooks(self):
        updatebooks2 = UpdateBooks2()
        widget.addWidget(updatebooks2)
        widget.setCurrentWidget(updatebooks2)

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

class UpdateBooks2(QDialog):
    def __init__(self):
        super(UpdateBooks2, self).__init__()
        loadUi("updateBooks2.ui", self)
        self.homeButton.clicked.connect(self.gotodash)
        self.logout.clicked.connect(self.gotologout)
        self.confirmbutton.clicked.connect(self.updateprocess)

#updating the record
    def updateprocess(self):
        try:
            newvalue = self.newrecordfield.text()
            category = self.categoryBox.currentText()
            if not newvalue:
                self.confirm.setText("Please enter the value to update.")
            else:
                if type(newvalue) is str:
                    cursor.execute("UPDATE Register SET {} = '{}' WHERE {} = {}".format(category, newvalue, updatecategory, updatesearchvalue))
                else:
                    cursor.execute("UPDATE Register SET {} = {} WHERE {} = {}".format(category, newvalue, updatecategory, updatesearchvalue))
                mydb.commit()
                self.confirm.setText("Record updated successfully!")
                cursor.execute("SELECT * FROM Register WHERE {} LIKE '%{}%'".format(updatecategory, updatesearchvalue))
                result = cursor.fetchall()
                self.registertable.setColumnCount(len(result[0]))
                self.registertable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.registertable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.registertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except mysql.connector.Error as Err:
            self.confirm.setText("Something went wrong. Try again after checking values.")

    def gotodash(self):
        dashboard = dashBoard()
        widget.addWidget(dashboard)
        widget.setCurrentWidget(dashboard)

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

#creating infobox class, displays info about our project
class InfoBox(QDialog):
    def __init__(self):
        super(InfoBox, self).__init__(parent=welcome)
        loadUi("info.ui", self)
        self.okButton.clicked.connect(self.gotoclose)

    def gotoclose(self):
        self.close()

#creating welcomescreen class, the main login screen which shows first
class WelcomeScreen(QMainWindow):
    #initializing and loading welcome screen
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcome.ui", self)
        self.infoButton.clicked.connect(self.gotoinfo)
        self.usernamefield.setPlaceholderText("Username")
        self.passwordfield.setPlaceholderText("Password")
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginbutton.clicked.connect(self.gotodashBoard)
        self.passwordfield.returnPressed.connect(self.gotodashBoard)
        self.newusersignup.clicked.connect(self.gotosignup)

    def gotoinfo(self):
        self.info = InfoBox()
        self.info.setWindowTitle("Info")
        self.info.show()

    def gotosignup(self):
        signup = SignUpScreen() 
        widget.addWidget(signup)
        widget.setCurrentWidget(signup)     

    #checking user credentials
    def gotodashBoard(self):
        global username
        username = self.usernamefield.text()
        password = self.passwordfield.text()

        if len(username)==0 or len(password)==0:
            self.error.setText("Please fill in all fields")
        
        else:
            query = "SELECT password FROM login_info WHERE username = '"+username+"'"
            cursor.execute(query)    
            result_pass = cursor.fetchone()

            if result_pass is not None:
                if result_pass[0] == password:
                    print("Successfully logged in.")
                    dashboard = dashBoard()
                    widget.addWidget(dashboard)
                    widget.setCurrentWidget(dashboard)
                else:
                    self.error.setText("Invalid username or password")
            else:
                self.error.setText("Invalid username or password")

#creating signupscreen class, users signup here
class SignUpScreen(QDialog):
    #initializing and loading signup screen
    def __init__(self):
        super(SignUpScreen, self).__init__()
        loadUi("signup.ui", self)
        self.signupname.setPlaceholderText("Name")
        self.signupuser.setPlaceholderText("Preferred username")
        self.signuppass.setPlaceholderText("Enter password")
        self.confirmpass.setPlaceholderText("Confirm password")
        self.signuppass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton.clicked.connect(self.gotosignup)
        self.backtologin.clicked.connect(self.gotologin)

    #logging out back to welcome screen
    def gotologin(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)
    
    #checking user credentials
    def gotosignup(self):
        global newname, newuser, newpass
        newname = self.signupname.text()
        newuser = self.signupuser.text()
        newpass1 = self.signuppass.text()
        newpass2 = self.confirmpass.text()

        if len(newname)== 0 or len(newuser) == 0 or len(newpass1) == 0 or len(newpass2) == 0:
            self.signuperror.setText("Please fill in all fields")

        elif newpass1 != newpass2:
            self.signuperror.setText("The passwords do not match")

        else:
            cursor.execute("SELECT * FROM login_info WHERE username = '"+newuser+"'")
            data = cursor.fetchall()
            if data:
                self.signuperror.setText("Username already exists")
            else:
                addnewquery = "INSERT IGNORE INTO login_info VALUES\
                    ('"+newname+"','"+newuser+"','"+newpass1+"')"
                cursor.execute(addnewquery)
                mydb.commit()
                self.signuperror.setText("Added new user to database. Successful!")

#creating clientscreen class
class ClientScreen(QDialog):	
    #initializing and loading client screen	
    def __init__(self):	
        super(ClientScreen, self).__init__()	
        loadUi("addClient.ui", self)	
        self.homeButton.clicked.connect(self.gotodash)	
        self.addButton.clicked.connect(self.addprocess)	
        self.logout.clicked.connect(self.gotologout)
        self.rnofield.setPlaceholderText("Roll number of client")
        self.namefield.setPlaceholderText("Name of the client")
        self.phonefield.setPlaceholderText("Phone number of client")
        self.efield.setPlaceholderText("EmailID of client")	

    #adding a new client
    def addprocess(self):	
        rno=self.rnofield.text()	
        name=self.namefield.text()	
        phone=self.phonefield.text()	
        email=self.efield.text()
        if not rno or not name or not phone:	
            if not rno:	
                self.value.setText("Please enter rollno.")	
            elif not name:	
                self.value.setText("Please enter the name of client")	
            elif not phone:	
                self.value.setText("Please enter the phone number of client")	
        else:
            cursor.execute("SELECT * FROM ClientInfo WHERE Roll_no = {}".format(rno, ))
            data = cursor.fetchall()
            if data:
                self.value.setText("Client already exists.")
            else:
                try:	
                    cursor.execute("INSERT INTO CLIENTINFO (Roll_no, Name, Phone, EmailID) VALUES({},'{}',{},'{}')".format(rno,name,phone,email))	
                    mydb.commit()	
                    self.value.setText("Client added successfully")	
                except mysql.connector.Error:
                    self.value.setText("Something went wrong. Please try again after checking all values.")

    def gotodash(self):	
        dashboard = dashBoard()	
        widget.addWidget(dashboard)	
        widget.setCurrentWidget(dashboard)	

    def gotologout(self):	
        welcome = WelcomeScreen()	
        widget.addWidget(welcome)	
        widget.setCurrentWidget(welcome)

#creating dashboard class, main dashboard from where one can navigate
class dashBoard(QDialog):
    #initialising and loading dashboard
    def __init__(self):
        super(dashBoard, self).__init__()
        loadUi("dashboard.ui", self)
        self.logout.clicked.connect(self.gotologout)
        self.updateButton.clicked.connect(self.gotoupdatemenu)
        self.registerButton.clicked.connect(self.gotoRegister)
        self.issueButton.clicked.connect(self.gotoissuebooks)
        self.clientButton.clicked.connect(self.gotoaddclient)
        cursor.execute("SELECT name FROM login_info WHERE username = '"+username+"'")
        greetname = cursor.fetchone()[0]
        self.name.setText("Hello "+greetname+"!")

    def gotologout(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentWidget(welcome)

    def gotoaddclient(self):	
        clientscreen=ClientScreen()	
        widget.addWidget(clientscreen)	
        widget.setCurrentWidget(clientscreen)

    def gotoRegister(self):
        reg = register()
        widget.addWidget(reg)
        widget.setCurrentWidget(reg)

    def gotoupdatemenu(self):
        updatebooks = UpdateMenu()
        widget.addWidget(updatebooks)
        widget.setCurrentWidget(updatebooks)

    def gotoissuebooks(self):
        issuebooks = IssueBooks()
        widget.addWidget(issuebooks)
        widget.setCurrentWidget(issuebooks)

#main
app = QtWidgets.QApplication(sys.argv)

widget = QStackedWidget()
widget.setWindowIcon(QtGui.QIcon("icon.png"))
welcome = WelcomeScreen()
signup = SignUpScreen()
widget.addWidget(welcome)
widget.addWidget(signup)
widget.setWindowTitle("VME Library Management")
widget.resize(1400, 750)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting..")
