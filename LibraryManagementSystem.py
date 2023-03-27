##############################################################################################################

# Import Section

##############################################################################################################

import psycopg2
import re
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from datetime import datetime
from datetime import date, timedelta
from argon2 import PasswordHasher
from prettytable import PrettyTable

# Establishing the connection
db = psycopg2.connect(
    database="LibraryManagementSystem",
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
)

cursor = db.cursor()
# print(cursor)
print("\t****************************** Library Management System ******************************\n")
##############################################################################################################

# Login Section

##############################################################################################################


def login(tableName):
    login_option = int(
        input("Enter Login Option : \n \t1. Email \n \t2. Mobile \n Select: "))
    if (login_option == 1):
        login_Email = input("Enter Your Email : ").lower()
        query_email = f"SELECT COUNT(email_id) FROM {tableName} WHERE email_id = '{login_Email}';"
        try:
            cursor.execute(query_email)
            data1 = cursor.fetchall()
            if (data1[0][0] > 0):
                password = input("Password : ")
                pass_query = f"SELECT password,mobile_number FROM {tableName} WHERE email_id = '{login_Email}';"
                try:
                    cursor.execute(pass_query)
                    old_password_data = cursor.fetchall()
                    ph = PasswordHasher()
                    if (ph.verify(old_password_data[0][0], password)):
                        email_id = login_Email
                        mobile = old_password_data[0][1]
                        # print(email_id)
                        # print(mobile)
                        list = ["1", mobile, email_id]
                        return list
                    else:
                        list = ["0"]
                        return list
                except Exception as e:
                    print(e)
            else:
                print("Wrong Email")
        except Exception as e:
            print(e)

    elif (login_option == 2):
        login_Mobile = input("Enter Your Mobile Number : ")
        query_mobile = f"SELECT COUNT(mobile_number) FROM {tableName} WHERE mobile_number = '{login_Mobile}';"
        try:
            cursor.execute(query_mobile)
            data2 = cursor.fetchall()
            if (data2[0][0] > 0):
                password = input("Password : ")
                pass_query = f"SELECT password,email_id FROM {tableName} WHERE mobile_number = '{login_Mobile}';"
                try:
                    cursor.execute(pass_query)
                    old_password_data = cursor.fetchall()
                    ph = PasswordHasher()
                    if (ph.verify(old_password_data[0][0], password)):
                        mobile = login_Mobile
                        email_id = old_password_data[0][1]
                        # print(email_id)
                        # print(mobile)
                        list = ["1", mobile, email_id]
                        return list
                    else:
                        list = ["0"]
                        return list
                except Exception as e:
                    print(e)
            else:
                print("Wrong Mobile Number")
        except Exception as e:
            print(e)

    else:
        print("You have choosen Wrong Input Please try again!!")

##############################################################################################################

        # Insert Section

##############################################################################################################


def insert(table_name):

    # First Name
    dummy = True
    fname = ""
    while (dummy):
        fname = input("First Name : ")
        if (fname == ''):
            print("Please Write Your First Name")
        elif fname.replace(" ", "").isalpha():
            dummy = False
        else:
            print("First Name Invalid Please Provide Valid First Name")

    # Last Name
    dummy = True
    lname = ""
    while (dummy):
        lname = input("Last Name : ")
        if (lname == ''):
            print("Please Write Your Last Name")
        elif lname.replace(" ", "").isalpha():
            dummy = False
        else:
            print("Last Name Invalid Please Provide Valid Last Name")

    # Mobile Number
    dummy = True
    mobile = ""
    while (dummy):
        mobile = input("Mobile Number : ")
        if (mobile_verification(mobile)):
            dummy = False
        else:
            print("Wrong Mobile Number Please Provide Valid Mobile Number")

    # Email
    dummy = True
    email = ""
    while (dummy):
        email = input("Email : ").lower()
        if (email_verification(email)):
            dummy = False
        else:
            print("Wrong Email Please Provide Valid Email")

    # Password
    dummy = True
    password = ""
    while (dummy):
        password = input("Password : ")
        if (password == ''):
            print("Please Write your Password")
            dummy = True
        elif (password_check(password)):
            encrypt_password = argon2_algo(password)
            dummy = False
        else:
            print("Passwords should be a combination of uppercase, lowercase, and numbers also include some special characters.")
            dummy = True

    # Address
    dummy = True
    address = ""
    while (dummy):
        address = input("Address : ")
        if (address == ''):
            dummy = False
        elif address.replace(" ", "").isalpha():
            dummy = False
        else:
            print("Address Invalid Please Provide Valid Address")

    # City
    dummy = True
    city = ""
    while (dummy):
        city = input("City : ")
        if (city == ''):
            dummy = False
        elif city.replace(" ", "").isalpha():
            dummy = False
        else:
            print("City Invalid Please Provide Valid City")

    # State
    dummy = True
    state = ""
    while (dummy):
        state = input("State : ")
        if (state == ''):
            dummy = False
        elif state.replace(" ", "").isalpha():
            dummy = False
        else:
            print("State Invalid Please Provide Valid State")

    # Country
    dummy = True
    country = ""
    while (dummy):
        country = input("Country : ")
        if (country == ''):
            dummy = False
        elif country.replace(" ", "").isalpha():
            dummy = False
        else:
            print("Country Invalid Please Provide Valid Country")

    # PinCode
    dummy = True
    pin_code = ""
    while (dummy):
        pin_code = input("PinCode : ")
        if (pin_code == ""):
            dummy = False
        if (pincode_verification(pin_code)):
            dummy = False
        else:
            print("Wrong Pin Code Please Provide Valid Pin Code")

    # DateOfBirth
    dummy = True
    dob = ""
    while (dummy):
        dob = input("Enter your date of birth in the format DD/MM/YYYY : ")
        if (is_valid_dob(dob)):
            dummy = False
        else:
            print("Incorrect DOB!")
            dummy = True

    # Query
    if (table_name == "staffTable"):
        Query = "INSERT INTO staffTable(first_name,last_name,mobile_number,email_id,password,address,city,state,country,pin_code,date_of_birth) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
            fname, lname, mobile, email, encrypt_password, address, city, state, country, pin_code, dob)
    elif (table_name == "userTable"):
        Query = "INSERT INTO userTable(first_name,last_name,mobile_number,email_id,password,address,city,state,country,pin_code,date_of_birth) VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
            fname, lname, mobile, email, encrypt_password, address, city, state, country, pin_code, dob)

    try:
        cursor.execute(Query)
        db.commit()
        print("Successful")
    except Exception as e:
        print(e)

# ========================================================================================================== #

# Email Verification


def email_verification(email):
    pat = "^[a-zA-Z0-9.+]+@[a-zA-Z0-9]+\.(com|co\.in|[a-zA-Z]+)$"
    if (email == ''):
        return False
    elif re.match(pat, email):
        return True
    return False

# ========================================================================================================== #

# Phone Number Verification


def mobile_verification(mobile):
    if (mobile == ''):
        return False
    elif (re.match(r"^(\+91[-\s]?)?[0]?[6789]\d{9}$", mobile)):
        return True
    return False

# ========================================================================================================== #


def pincode_verification(pin_code):
    if (pin_code == ''):
        return False
    elif (re.fullmatch("\d{4}|\d{6}", pin_code)):
        return True
    return False

# ========================================================================================================== #


def argon2_algo(password):
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    hash = ph.hash(password)
    return hash

# ==========================================================================================================


def is_valid_dob(dob_str):
    # convert the string to a date object
    try:
        dob = datetime.strptime(dob_str, "%d/%m/%Y").date()
    except ValueError:
        print("Incorrect date format, should be DD/MM/YYYY")
        return False

    # check if the date is in the past
    if dob >= date.today():
        print("Date of birth should be in the past")
        return False

    # check if the date is not more than 150 years ago
    if dob <= date.today() - timedelta(days=365.25 * 150):
        print("Age should not be greater than 150 years")
        return False

    return True
# ==========================================================================================================


def password_check(password):
    # check length of password
    if len(password) < 8:
        return False

    # check if password has at least one digit
    if not any(char.isdigit() for char in password):
        return False

    # check if password has at least one lowercase letter
    if not any(char.islower() for char in password):
        return False

    # check if password has at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False

    # check if password has at least one special character
    special_characters = "!@#$%^&*()_+-=[]{};:,.<>/?`~"
    if not any(char in special_characters for char in password):
        return False

    # if all conditions are met, return True
    return True

def add_30_days(date_str):
    # Convert input date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Add 30 days to the datetime object
    new_date_obj = date_obj + timedelta(days=30)
    
    # Format the new date object as a string in the same format as the input
    new_date_str = datetime.strftime(new_date_obj, "%Y-%m-%d")
    
    # Return the new date string
    return new_date_str
##############################################################################################################

    # Create Table Section

##############################################################################################################


def create_Table_Staff():
    cursor.execute("CREATE TABLE staffTable(id SERIAL PRIMARY KEY,first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,mobile_number varchar(15) UNIQUE,email_id varchar(100) UNIQUE,password varchar(100),address varchar(50),city varchar(50),state varchar(50),country varchar(50),pin_code varchar(10),date_of_birth varchar(10),status int DEFAULT 1)")
    db.commit()
    print("Table created staffTable!!")
# create_Table_Staff()


def create_Table_User():
    cursor.execute("CREATE TABLE userTable(id SERIAL PRIMARY KEY,first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,mobile_number varchar(15) UNIQUE,email_id varchar(100) UNIQUE,password varchar(100),address varchar(50),city varchar(50),state varchar(50),country varchar(50),pin_code varchar(10),date_of_birth varchar(10),status int DEFAULT 1)")
    db.commit()
    print("Table created userTable!!")
# create_Table_User()


def book_Records():
    cursor.execute("CREATE TABLE bookRecords(bookid SERIAL PRIMARY KEY,staff_id VARCHAR(5) NOT NULL, book_name VARCHAR(100) NOT NULL UNIQUE,book_author VARCHAR(100) NOT NULL,quantity varchar(5),status int DEFAULT 1)")
    db.commit()
    print("Table created bookRecords!!")
# book_Records()


def book_Issue():
    cursor.execute("CREATE TABLE bookissue(userid varchar(5) NOT NULL,book_name VARCHAR(100) NOT NULL,book_author VARCHAR(100) NOT NULL,quantity varchar(5),status int DEFAULT 1)")
    db.commit()
    print("Table created book_Issue!!")
# book_Issue()


def book_Return():
    cursor.execute("CREATE TABLE bookReturn(userid varchar(5) NOT NULL,book_name VARCHAR(100) NOT NULL,book_author VARCHAR(100) NOT NULL,quantity varchar(5),status int DEFAULT 1)")
    db.commit()
    print("Table created book_Return!!")
# book_Return()

##############################################################################################################

    # Main Section

##############################################################################################################


identity_check = int(input(
    "\t\t\t******** Select your Identity or Preferences ******** \n \t1. Staff \n \t2. User \n Select: "))

if (identity_check == 1):
    # Staff Section Code
    Staff_login_option = int(input("\t\t\t\t******** First you need to login ******** \n \t1. Login \n \t2. Create a Account \n Select 1 or 2 : "))
    staffTable = "staffTable"
    if (Staff_login_option == 1):
        print("\t\t\t\t\t******** Login ********")
        list = login(staffTable)
        if (list[0] == "1"):
            staff_Option = int(input("\nWhat You want to do is either add or remove the book.\n \t1. Add \n \t2. Remove \n  \t3. Status or Collection of books in library \n Select: "))
            if (staff_Option == 1):
                staffID_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(staffID_Query)
                    staffID_data = cursor.fetchall()
                    # print(list[1])
                    staffID = staffID_data[0][0]
                    # print(staffID)
                    book_Name = input("Enter book name: ").lower()
                    book_Author = input("Enter book author name: ").lower()
                    book_Quantity = int(input("Enter book Quantity: "))
                    book_Records_Check_Querry1 = "SELECT COUNT(book_name) FROM bookRecords WHERE book_name = '{}';".format(
                        book_Name)
                    book_Records_Check_Querry2 = "SELECT quantity FROM bookRecords WHERE book_name = '{}';".format(
                        book_Name)
                    book_Records_Check_Querry3 = "SELECT COUNT(book_author) FROM bookRecords WHERE book_author = '{}';".format(
                        book_Author)
                    try:
                        cursor.execute(book_Records_Check_Querry1)
                        book_records_data1 = cursor.fetchall()
                        cursor.execute(book_Records_Check_Querry2)
                        book_records_data2 = cursor.fetchall()
                        cursor.execute(book_Records_Check_Querry3)
                        book_records_data3 = cursor.fetchall()
                        if (book_records_data1[0][0] > 0 and book_records_data3[0][0] > 0):
                            book_Records_Querry = "UPDATE bookRecords SET quantity = '{}' WHERE book_name = '{}' AND book_author = '{}';".format(book_Quantity+book_records_data2[0][0], book_Name, book_Author)
                            try:
                                cursor.execute(book_Records_Querry)
                                # print("Same")
                                db.commit()
                            except Exception as e:
                                print(e)
                        else:
                            book_Records_Querry = "INSERT INTO bookRecords(staff_id,book_name,book_author,quantity) VALUES('{}','{}','{}','{}');".format(
                                staffID, book_Name, book_Author, book_Quantity)
                            try:
                                cursor.execute(book_Records_Querry)
                                db.commit()
                                # print(book_Name)
                                # print("Differ")
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)

            elif (staff_Option == 2):
                Remove_Book_Name = input("Enter Book Name and Author Name that you want to remove \n1. Book Name: ")
                Remove_Author_Name = input("2. Book Author Name: ")
                staffID_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{list[1]}';"
                try:
                    print("1")
                    cursor.execute(staffID_Query)
                    staffID_data = cursor.fetchall()
                    staffID = staffID_data[0][0]
                    print("2")
                    check_remove_book_query = "SELECT COUNT(book_name) FROM bookRecords WHERE book_name = '{}' AND book_author = '{}' AND staff_id = '{}'".format(Remove_Book_Name,Remove_Author_Name,staffID)
                    try:
                        print("3")
                        cursor.execute(check_remove_book_query)
                        check_remove_book_query_data = cursor.fetchall()
                        print(check_remove_book_query_data[0])
                        if(check_remove_book_query_data[0][0]>0):
                            print("5")
                            Remove_Book_Query = "UPDATE bookRecords SET status = '{}' WHERE book_name = '{}' AND book_author = '{}' AND staff_id = '{}'".format(2,Remove_Book_Name,Remove_Author_Name,staffID)
                            try:
                                print("6")
                                cursor.execute(Remove_Book_Query)
                                db.commit()
                                print("7")
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                
            elif(staff_Option == 3):
                staff_status_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(staff_status_Query)
                    staff_status_data = cursor.fetchall()
                    staff_status_UserID = staff_status_data[0][0]
                    sta_Query = f"SELECT book_name,book_author,quantity FROM bookrecords WHERE staff_id = '{staff_status_UserID}' AND status = '1';"
                    cursor.execute(sta_Query)
                    # fetch all rows of data from the SELECT statement
                    rows = cursor.fetchall()
                    # create a PrettyTable object and set the column names
                    table = PrettyTable(['Book Name','Book Author','Quantity'])
                    # iterate through the rows of data and add them to the table
                    for row in rows:
                        table.add_row(row)
                    # print the table
                    print(table)
                except Exception as e:
                    print(e)
            else:
                print("You have choosen Wrong Input Please try again!!")
        else:
            print("Try Again!!")
    elif (Staff_login_option == 2):
        print("\t\t\t\t******** Create an account ********")
        insert(staffTable)
    else:
        print("You have choosen Wrong Input Please try again!!")

elif (identity_check == 2):
    # User Section Code
    User_login_option = int(input("########## First you need to login ########## \n 1. Login \n 2. Create a Account \n Select 1 or 2 : "))
    userTable = "userTable"
    if (User_login_option == 1):
        print("########## Login ##########")
        list = login(userTable)
        if (list[0] == "1"):
            user_Option = int(input("What You want to do is either book issue or return the book.\n 1. Book Issue \n 2. Return Book \n 3. Status of your account \n Select: "))
            if (user_Option == 1):
                user_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(user_Query)
                    user_data = cursor.fetchall()
                    userID = user_data[0][0]
                    book_Name = input("Enter book name: ").lower()
                    book_Author = input("Enter book author name: ").lower()
                    book_Quantity = int(input("Enter book Quantity: "))
                    book_Issue_Check_Querry1 = "SELECT book_name, book_author, quantity FROM bookRecords WHERE book_name = '{}' AND book_author = '{}';".format(book_Name, book_Author)
                    book_Issue_Check_Querry2 = "SELECT COUNT(book_name) FROM bookIssue WHERE book_name = '{}' AND book_author = '{}' AND userid = '{}';".format(book_Name, book_Author,userID)
                    book_Issue_Check_Querry3 = "SELECT quantity FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(book_Name, book_Author)
                    try:
                        cursor.execute(book_Issue_Check_Querry1)
                        book_Issue_data1 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry2)
                        book_Issue_data2 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry3)
                        book_Issue_data3 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry1)
                        # print("1")
                        if (cursor.fetchone() is not None):
                            # print("2")
                            if (book_Issue_data1[0][0] == book_Name and book_Issue_data1[0][1] == book_Author):
                                # print("3")
                                if ((int(book_Quantity)) <= book_Issue_data1[0][2]):
                                    # print("4")
                                    if (book_Issue_data2[0][0] > 0):
                                        if ((int(book_Quantity)+ int(book_Issue_data3[0][0]) <= book_Issue_data1[0][2])):
                                            # print("5")
                                            book_Issue_Querry = "UPDATE bookIssue SET quantity = '{}' WHERE book_name = '{}' AND book_author = '{}' AND userid = '{}';".format(int(book_Quantity)+int(book_Issue_data3[0][0]), book_Name, book_Author,userID)
                                            try:
                                                cursor.execute(book_Issue_Querry)
                                                db.commit()
                                                # cursor.execute("CREATE TRIGGER set_BookIssueDate BEFORE INSERT ON BookIssue FOR EACH ROW EXECUTE FUNCTION set_BookIssueDate()")
                                                # # execute a CREATE FUNCTION statement to define the 'set_BookIssueDate' function that sets the value of the 'BookIssueDate' column to the current date
                                                # cursor.execute("""
                                                # CREATE OR REPLACE FUNCTION set_BookIssueDate()
                                                # RETURNS TRIGGER AS $$
                                                # BEGIN
                                                #     NEW.BookIssueDate := CURRENT_DATE;
                                                #     RETURN NEW;
                                                # END;
                                                # $$ LANGUAGE plpgsql;
                                                # """)
                                                # # commit the transaction to make the changes permanent
                                                # db.commit()
                                                book_Issue_Date = "SELECT bookissuedate FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(book_Name, book_Author)
                                                try:
                                                    cursor.execute(book_Issue_Date)
                                                    book_Issue_Date_Data = cursor.fetchall()
                                                    book_Due_Date = add_30_days(book_Issue_Date_Data[0][0])
                                                    book_Due = "Update bookIssue SET duedate = '{}' Where book_name = '{}' AND book_author = '{}';".format(book_Due_Date,book_Name, book_Author)
                                                    try:
                                                        cursor.execute(book_Due)
                                                        db.commit
                                                    except Exception as e:
                                                        print(e)
                                                except Exception as e:
                                                    print(e)
                                            except Exception as e:
                                                print(e)
                                        else:
                                            print("That quantity of books are not available to this library please search on other library.")

                                    else:
                                        # print("6")
                                        book_Issue_Querry = "INSERT INTO bookIssue(userid,book_name,book_author,quantity) VALUES('{}','{}','{}','{}');".format(userID, book_Name, book_Author, book_Quantity)
                                        try:
                                            # print("7")
                                            cursor.execute(book_Issue_Querry)
                                            db.commit()
                                            # cursor.execute("CREATE TRIGGER set_BookIssueDate BEFORE INSERT ON BookIssue FOR EACH ROW EXECUTE FUNCTION set_BookIssueDate()")
                                            # # execute a CREATE FUNCTION statement to define the 'set_BookIssueDate' function that sets the value of the 'BookIssueDate' column to the current date
                                            # cursor.execute("""
                                            # CREATE OR REPLACE FUNCTION set_BookIssueDate()
                                            # RETURNS TRIGGER AS $$
                                            # BEGIN
                                            #     NEW.BookIssueDate := CURRENT_DATE;
                                            #     RETURN NEW;
                                            # END;
                                            # $$ LANGUAGE plpgsql;
                                            # """)
                                            # # commit the transaction to make the changes permanent
                                            # db.commit()
                                            
                                            # book_Issue_Date = "SELECT bookissuedate FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(book_Name, book_Author)
                                            # try:
                                            #     cursor.execute(book_Issue_Date)
                                            #     book_Issue_Date_Data = cursor.fetchall()
                                            #     book_Due_Date = add_30_days(book_Issue_Date_Data[0][0])
                                            #     book_Due = "Update bookIssue SET duedate = '{}' Where book_name = '{}' AND book_author = '{}';".format(book_Due_Date,book_Name, book_Author)
                                            #     try:
                                            #         cursor.execute(book_Due)
                                            #         db.commit
                                            #     except Exception as e:
                                            #         print(e)
                                            # except Exception as e:
                                            #     print(e)
                                            
                                        except Exception as e:
                                            print(e)
                                else:
                                    print("That quantity of books are not available to this library please search on other library.")
                        else:
                            print("This book are not available in my library please search on other library.")
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
            elif (user_Option == 2):
                user_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(user_Query)
                    user_data = cursor.fetchall()
                    userID = user_data[0][0]
                    book_Name = input("Enter book name: ").lower()
                    book_Author = input("Enter book author name: ").lower()
                    book_Quantity = int(input("Enter book Quantity: "))
                    book_Issue_Check_Querry1 = "SELECT book_name, book_author, quantity FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(
                        book_Name, book_Author)
                    book_Issue_Check_Querry2 = "SELECT COUNT(book_name) FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(
                        book_Name, book_Author)
                    book_Issue_Check_Querry3 = "SELECT quantity FROM bookIssue WHERE book_name = '{}' AND book_author = '{}';".format(
                        book_Name, book_Author)
                    try:
                        cursor.execute(book_Issue_Check_Querry1)
                        book_Issue_data1 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry2)
                        book_Issue_data2 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry3)
                        book_Issue_data3 = cursor.fetchall()
                        cursor.execute(book_Issue_Check_Querry1)
                        if (cursor.fetchone() is not None):
                            if (book_Issue_data1[0][0] == book_Name and book_Issue_data1[0][1] == book_Author):
                                if ((int(book_Issue_data3[0][0]) - int(book_Quantity)) >= 0):
                                    if (book_Issue_data2[0][0] > 0):
                                        book_Issue_Querry = "UPDATE bookIssue SET quantity = '{}' WHERE book_name = '{}' AND book_author = '{}';".format(int(book_Issue_data3[0][0]) - int(book_Quantity), book_Name, book_Author)
                                        try:
                                            cursor.execute(book_Issue_Querry)
                                            db.commit()
                                        except Exception as e:
                                            print(e)
                                else:
                                    print("That quantity of books are not from this library please return this book to other library.")
                        else:
                            print("This book are not from this library please go on other library.")
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
            elif(user_Option==3):
                status_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(status_Query)
                    status_data = cursor.fetchall()
                    status_UserID = status_data[0][0]
                    sta_Query = f"SELECT book_name,book_author,quantity,fine,duedate,bookissuedate FROM bookIssue WHERE userid = '{status_UserID}';"
                    cursor.execute(sta_Query)
                    # fetch all rows of data from the SELECT statement
                    rows = cursor.fetchall()
                    # create a PrettyTable object and set the column names
                    table = PrettyTable(['Book Name','Book Author','Quantity','Fine','Due Date','Book Issue Date'])
                    # iterate through the rows of data and add them to the table
                    for row in rows:
                        table.add_row(row)
                    # print the table
                    print(table)
                except Exception as e:
                    print(e)
            else:
                print("You have choosen Wrong Input Please try again!!")
    elif (User_login_option == 2):
        print("########## Create an account ##########")
        insert(userTable)
    else:
        print("You have choosen Wrong Input Please try again!!")
else:
    print("You have choosen Wrong Input Please try again!!")






##############################################################################################################

    # Extra Code That I have Used

##############################################################################################################

# CREATE DATABASE LibraryManagementSystem OWNER ujjawal;
# \l  -> Show all Databases
# \c  -> Use Databases
# \dt -> Show all tables in one databases
# ALTER TABLE bookissue OWNER TO ujjawal;
# ALTER TABLE bookrecords OWNER TO ujjawal;
# ALTER TABLE bookreturn OWNER TO ujjawal;
# ALTER TABLE stafftable OWNER TO ujjawal;
# ALTER TABLE usertable OWNER TO ujjawal;
# UPDATE bookrecords SET book_name = 'python crash course' WHERE bookid = 1 RETURNING *;
# Alter table bookrecords ALTER COLUMN quantity TYPE INTEGER USING quantity::integer;
# ALTER TABLE bookrecords DROP COLUMN staff_id;
# ALTER TABLE bookreturn ADD PRIMARY KEY (id);
# ALTER TABLE bookreturn ADD COLUMN id SERIAL;
