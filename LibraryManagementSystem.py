##############################################################################################################

# Import Section

##############################################################################################################

import psycopg2
import re
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
import datetime as dt
from datetime import datetime
from datetime import date, timedelta
from argon2 import PasswordHasher
from prettytable import PrettyTable
# import argon2.exceptions.VerificationError
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

                                         # Fine Section

##############################################################################################################


def fine():
    cursor.execute('SELECT bookissuedate, duedate, fine FROM bookissue')
    rows = cursor.fetchall()
    for row in rows:
        if row[1] is None:
            continue  # Skip this row and move on to the next one
        duedate_str = row[1].strftime('%Y-%m-%d')
        duedate = datetime.strptime(duedate_str, '%Y-%m-%d').date()
        current_date = date.today()
        if current_date > duedate:
            days_late = (current_date - duedate).days
            fine = days_late * 5  # assuming a fine of Rs. 5 per day
        else:
            fine = 0
        cursor.execute(
            "UPDATE bookissue SET fine=%s WHERE bookissuedate=%s AND duedate=%s", (fine, row[0], row[1]))
    db.commit()


fine()

##############################################################################################################

                                         # Login Section

##############################################################################################################


def login(tableName):
    login_option = int(
        input("Enter Login Option : \n \t1. Email \n \t2. Mobile\n Select: "))
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

                                                    # Insert & Update Section

##############################################################################################################


def update_Password(tableName):
    ans = input("Do You Want to change Your Password : (Y/N) ")
    if (ans == "Y" or ans == "y"):
        option_password = int(input(
            "We must first confirm that you are a genuine person or not, \n Please select these option \n 1. Email \n 2. Mobile \n 3. Old Password \n Enter : "))

        # Update Password Using Email and the DOB
        if (option_password == 1):
            print("Update Password Using Email")
            email_id = input("Email : ").lower()
            update_query_email = f"SELECT COUNT(email_id) FROM {tableName} WHERE email_id = '{email_id}'"
            try:
                cursor.execute(update_query_email)
                result = cursor.fetchone()
                email_id_data = result[0]
                if (email_id_data > 0):
                    email_dob = input(
                        "Enter your Date of Birth (DD/MM/YYYY) : ")
                    pass_query = "SELECT password FROM {} WHERE email_id = '{}';".format(tableName, email_id)
                    try:
                        cursor.execute(pass_query)
                        old_password_data = cursor.fetchall()
                        ph = PasswordHasher()
                        email_dob_query = f"SELECT date_of_birth FROM {tableName} WHERE email_id = '{email_id}';"
                        try:
                            cursor.execute(email_dob_query)
                            email_dob_data = cursor.fetchall()
                            if (email_dob_data[0][0] == email_dob):
                                dummy = True
                                email_password1 = ''
                                while (dummy):
                                    email_password1 = input("New Password : ")
                                    try:
                                        if (ph.verify(old_password_data[0][0], email_password1)):
                                            print("Password is same please try again!!!")
                                            dummy = False
                                            break
                                    except Exception as e:
                                        # print(e)
                                        pass
                                    email_password2 = input("Confirm Password : ")
                                    if (email_password1 == email_password2):
                                        if (email_password1 == ''):
                                            print("Please Write your Password")
                                            dummy = True
                                        elif (password_check(email_password1)):
                                            email_encrypt_new_password = argon2_algo(
                                                email_password1)
                                            email_pass_query = f"UPDATE {tableName} SET password = '{email_encrypt_new_password}' WHERE email_id = '{email_id}' AND date_of_birth = '{email_dob}';"
                                            try:
                                                cursor.execute(email_pass_query)
                                                db.commit()
                                                print("Successful")
                                            except Exception as e:
                                                print("Error!!")
                                            dummy = False
                                        else:
                                            dummy = True
                                    else:
                                        print(
                                            "Your new password and confirm password are not same..")
                            else:
                                print("Wrong DOB!")
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                else:
                    print("Wrong Email")
            except Exception as e:
                print("Error executing query: {}".format(str(e)))

        # Update Password Using Mobile Number and then DOB
        elif (option_password == 2):
            print("Update Password Using Mobile Number : ")
            mobile_number = input("Mobile Number : ")
            update_query_mobile = "SELECT COUNT(mobile_number) FROM {} WHERE mobile_number = '{}';".format(tableName, mobile_number)
            try:
                # print("1")
                cursor.execute(update_query_mobile)
                # print("2")
                mobile_number_data = cursor.fetchall()
                # print("3")
                if (mobile_number_data[0][0] > 0):
                    # print("4")
                    pass_query = "SELECT password FROM {} WHERE mobile_number = '{}';".format(tableName, mobile_number)
                    try:
                        # print("5")
                        cursor.execute(pass_query)
                        old_password_data = cursor.fetchall()
                        ph = PasswordHasher()
                        mob_dob = input("Enter your Date of Birth (DD/MM/YYYY) : ")
                        mob_dob_query = "SELECT date_of_birth FROM {} WHERE mobile_number = '{}';".format(
                            tableName, mobile_number)
                        try:
                            cursor.execute(mob_dob_query)
                            mob_dob_data = cursor.fetchall()
                            if (mob_dob_data[0][0] == mob_dob):
                                dummy = True
                                mob_password1 = ''
                                while (dummy):
                                    mob_password1 = input("New Password : ")
                                    try:
                                        if (ph.verify(old_password_data[0][0], mob_password1)):
                                            print("Password is same please try again!!!")
                                            dummy = False
                                            break
                                    except Exception as e:
                                        # print(e)
                                        pass
                                    
                                        
                                    mob_password2 = input("Confirm Password : ")
                                    if (mob_password1 == mob_password2):
                                        if (mob_password1 == ''):
                                            print("Please Write your Password")
                                            dummy = True
                                        elif (password_check(mob_password1)):
                                            mob_encrypt_new_password = argon2_algo(
                                                mob_password1)
                                            mob_pass_query = "UPDATE {} SET password = '{}' WHERE mobile_number = '{}' AND date_of_birth = '{}';".format(
                                                tableName, mob_encrypt_new_password, mobile_number, mob_dob)
                                            # print(mob_pass_query)
                                            try:
                                                cursor.execute(mob_pass_query)
                                                db.commit()
                                                
                                                print("Successful")
                                            except Exception as e:
                                                print("Error!!")
                                            dummy = False
                                        else:
                                            dummy = True
                                    else:
                                        print(
                                            "Your new password and confirm password are not same..")
                            else:
                                print("Wrong Password!")
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                else:
                    print("Wrong Mobile Number")
            except Exception as e:
                print("Error")

        #  Update Password Using Old Password
        elif (option_password == 3):
            print("First you need to login : ")
            email_login = input("Email : ").lower()
            login_querry = "SELECT COUNT(email_id) FROM {} WHERE email_id = '{}';".format(
                tableName, email_login)
            try:
                cursor.execute(login_querry)
                data1 = cursor.fetchall()
                if (data1[0][0] > 0):
                    password_login = input("Old Password : ")
                    pass_query = "SELECT password FROM {} WHERE email_id = '{}';".format(
                        tableName, email_login)
                    try:
                        cursor.execute(pass_query)
                        old_password_data = cursor.fetchall()
                        ph = PasswordHasher()
                        password1 = ''
                        if (ph.verify(old_password_data[0][0], password_login)):
                            dummy = True
                            while (dummy):
                                password1 = input("New Password : ")
                                if(password1==password_login):
                                    print("Your Old Password and New Password is same.")
                                    dummy = False
                                    break
                                password2 = input("Confirm Password : ")
                                if (password1 == password2):
                                    if (password1 == ''):
                                        print("Please Write your Password")
                                        dummy = True
                                    elif (password_check(password1)):
                                        encrypt_new_password = argon2_algo(
                                            password1)
                                        old_password_query = "UPDATE {} SET password = '{}' WHERE email_id = '{}' AND password = '{}';".format(
                                            tableName, encrypt_new_password, email_login, old_password_data[0][0])
                                        try:
                                            cursor.execute(old_password_query)
                                            db.commit()
                                            print("Successful")
                                        except Exception as e:
                                            print("Error!!")
                                        dummy = False
                                    else:
                                        dummy = True
                                else:
                                    print(
                                        "Your new password and confirm password are not same..")
                        else:
                            print("Wrong Password!")
                    except Exception as e:
                        print(e)
                else:
                    print("Wrong Email")
            except Exception as e:
                print("Error")

    elif (ans == 'N' or ans == 'n'):
        print("Good Habbit!! Don't Forget Your Password")
    else:
        print("Please choose correct option...")

# =========================================== Insert Section for Staff & User =========================================

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

# ==============================================Super Admin insert Section=========================================================== #


def insertsuperadmin():

    # First Name
    dummy = True
    fname = ""
    while (dummy):
        fname = input("First Name : ").lower().strip()
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
        lname = input("Last Name : ").lower().strip()
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
        mobile = input("Mobile Number : ").strip()
        if (mobile_verification(mobile)):
            dummy = False
        else:
            print("Wrong Mobile Number Please Provide Valid Mobile Number")

    # Email
    dummy = True
    email = ""
    while (dummy):
        email = input("Email : ").lower().strip()
        if (email_verification(email)):
            dummy = False
        else:
            print("Wrong Email Please Provide Valid Email")

    # Password
    dummy = True
    password = ""
    while (dummy):
        password = input("Password : ").strip()
        if (password == ''):
            print("Please Write your Password")
            dummy = True
        elif (password_check(password)):
            encrypt_password = argon2_algo(password)
            dummy = False
        else:
            print("Passwords should be a combination of uppercase, lowercase, and numbers also include some special characters.")
            dummy = True

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
    Query = "INSERT INTO superadmin(first_name,last_name,mobile_number,email_id,password,date_of_birth) VALUES('{}','{}','{}','{}','{}','{}');".format(
            fname, lname, mobile, email, encrypt_password, dob)

    try:
        cursor.execute(Query)
        db.commit()
        print("Successful")
    except Exception as e:
        print(e)


# ==============================================Email Verification============================================================ #

def email_verification(email):
    pat = "^[a-zA-Z0-9.+]+@[a-zA-Z0-9]+\.(com|co\.in|[a-zA-Z]+)$"
    if (email == ''):
        return False
    elif re.match(pat, email):
        return True
    return False

# =========================================== Phone Number Verification ========================================================== #

def mobile_verification(mobile):
    if (mobile == ''):
        return False
    elif (re.match(r"^(\+91[-\s]?)?[0]?[6789]\d{9}$", mobile)):
        return True
    return False

# =============================================== Pin Code Verification =================================== #


def pincode_verification(pin_code):
    if (pin_code == ''):
        return False
    elif (re.fullmatch("\d{4}|\d{6}", pin_code)):
        return True
    return False

# ============================================ Password Verification ========================================== #


def argon2_algo(password):
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    hash = ph.hash(password)
    return hash

# ============================================ Validate date Of Birth =============================================


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


# ======================================== Password Check ===============================================#


def password_check(password):
    # check length of password
    if len(password) < 8:
        print("Please make the password length minimum 8!!")
        return False
    if ' ' in password:
        print("Remove Space from password!!")
        return False
    # check if password has at least one digit
    if not any(char.isdigit() for char in password):
        print("Please add atleast one digit!!")
        return False

    # check if password has at least one lowercase letter
    if not any(char.islower() for char in password):
        print("Please add atleast one lowercase letter!!")
        return False

    # check if password has at least one uppercase letter
    if not any(char.isupper() for char in password):
        print("Please add atleast one uppercase letter!!")
        return False

    # check if password has at least one special character
    special_characters = "!@#$%^&*()_+-=[]{};:,.<>/?`~"
    if not any(char in special_characters for char in password):
        print("Please add atleast one special character!!")
        return False

    # if all conditions are met, return True
    return True

# ======================================== Add Due Date Function ===============================================

def add_due_date(date_str, extenddate):
    # Convert input date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y/%m/%d")

    # Add 30 days to the datetime object
    new_date_obj = date_obj + timedelta(days=extenddate)

    # Format the new date object as a string in the same format as the input
    new_date_str = datetime.strftime(new_date_obj, "%Y/%m/%d")

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
    "\t\t\t******** Select your Identity or Preferences ******** \n \t1. Super Admin \n \t2. Staff \n \t3. User \n Select: "))

############################################################################################################

                                            # Super Admin Section

############################################################################################################

# Create table
# CREATE TABLE superadmin(id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,mobile_number varchar(15) UNIQUE,email_id varchar(100) UNIQUE,password varchar(100));

# Call insertsuperadmin function to add superadmin
# insertsuperadmin()

# Add User and Staff
if(identity_check==1):
    superadmin = "superadmin"
    list = login(superadmin)
    if (list[0] == "1"):
        superadmin_option = int(input("\n Add acccount and check status of books \n 1. Add Staff \n 2. Add User \n 3. Add Book \n 4. Remove Book \n 5. Remove Staff \n 6. Remove User \n 7. Check Status of particular staff \n 8. Check Status according to user \n \n Select: "))
        if (superadmin_option == 1):
            print("\n Add Staff \n")
            staff = "staffTable"
            insert(staff)
        elif (superadmin_option == 2):
            print("\n Add User \n")
            user = "userTable"
            insert(user)
        elif (superadmin_option == 3):
            print("\n Add Book \n")
            admin_status_Query = f"SELECT book_name,book_author,quantity FROM bookrecords where status= '1';"
            try:
                cursor.execute(admin_status_Query)
                # fetch all rows of data from the SELECT statement
                rows = cursor.fetchall()
                # create a PrettyTable object and set the column names
                table = PrettyTable(['Book Name', 'Book Author', 'Quantity'])
                # iterate through the rows of data and add them to the table
                for row in rows:
                    table.add_row(row)
                # print the table
                print(table)
            except Exception as e:
                print(e)


            book_Name = input("\nEnter book name: ").lower().strip()
            book_Author = input("Enter book author name: ").lower().strip()
            book_Quantity = int(input("Enter book Quantity: "))
            book_category = int(input("Select your book category from these given options: \n \n1. Newspaper\n2. Magzine \n3. Engineering Book \n4. Medical Book \n5. Story Book \n6. Research Paper \n7. Classical Book \n8. Rommance Book \n9. Kids Book \n10. Arts Book \n11. Thrillers Book \n12. Text Books \n13. Finance \n14. Trending Books \n\nChoose option: "))
            book_category_name = ""
            extend = 0
            if (book_category == 1):
                book_category_name = "newspaper"
                extend = 1
            elif (book_category == 2):
                book_category_name = "magzine"
                extend = 5
            elif (book_category == 3):
                book_category_name = "enginnering"
                extend = 30
            elif (book_category == 4):
                book_category_name = "medical"
                extend = 30
            elif (book_category == 5):
                book_category_name = "story"
                extend = 15
            elif (book_category == 6):
                book_category_name = "research paper"
                extend = 3
            elif (book_category == 7):
                book_category_name = "classical"
                extend = 7
            elif (book_category == 8):
                book_category_name = "rommance"
                extend = 7
            elif (book_category == 9):
                book_category_name = "kids"
                extend = 7
            elif (book_category == 10):
                book_category_name = "arts"
                extend = 7
            elif (book_category == 11):
                book_category_name = "trillers"
                extend = 7
            elif (book_category == 12):
                book_category_name = "text book"
                extend = 7
            elif (book_category == 13):
                book_category_name = "finance"
                extend = 15
            elif (book_category == 14):
                book_category_name = "trending book"
                extend = 15
            else:
                book_category_name = "Unknown"
                extend = 5
            if (book_Quantity < 0):
                print("You have enter -ve quantity of books.")
            elif (book_category < 0 and book_category != 0):
                print("You have enter invalid number.")
            else:
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
                        book_Records_Querry = "UPDATE bookRecords SET quantity = '{}',category = '{}' WHERE book_name = '{}' AND book_author = '{}' AND status= '1';".format(
                                                    book_Quantity+book_records_data2[0][0], book_category_name, book_Name, book_Author)
                        try:
                            cursor.execute(book_Records_Querry)
                            # print("Same")
                            db.commit()
                        except Exception as e:
                            print(e)
                    else:
                        book_Records_Querry = "INSERT INTO bookRecords(staff_id,book_name,book_author,quantity,category) VALUES('{}','{}','{}','{}','{}');".format(
                                                    0, book_Name, book_Author, book_Quantity, book_category_name)
                        try:
                            cursor.execute(book_Records_Querry)
                            db.commit()
                            # print(book_Name)
                            # print("Differ")
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)

        elif (superadmin_option == 4):
            print("\n Remove Book \n")
            Remove_Book_Name = input("Enter Book Name and Author Name that you want to remove \n1. Book Name: ").lower().strip()
            Remove_Author_Name = input("2. Book Author Name: ").lower().strip()
            check_remove_book_query = "SELECT COUNT(book_name) FROM bookRecords WHERE book_name = '{}' AND book_author = '{}' AND status = '1'".format(Remove_Book_Name, Remove_Author_Name)
            try:
                # print("3")
                cursor.execute(check_remove_book_query)
                check_remove_book_query_data = cursor.fetchall()
                # print(check_remove_book_query_data[0])
                if (check_remove_book_query_data[0][0] > 0):
                    # print("5")
                    Remove_Book_Query = "UPDATE bookRecords SET status = '{}' WHERE book_name = '{}' AND book_author = '{}' AND status= '1'".format(2, Remove_Book_Name, Remove_Author_Name)
                    try:
                        # print("6")
                        cursor.execute(Remove_Book_Query)
                        db.commit()
                        print("Remove Book from library.")
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
        
        elif (superadmin_option == 5):
            print("\n remove Staff \n")
            Remove_Staff_Mobile = input("Enter Staff mobile number:  ").strip()
            Remove_Staff_Query = "UPDATE stafftable SET status = '{}' WHERE mobile_number = '{}' AND status= '1'".format(
                2, Remove_Staff_Mobile)
            try:
                cursor.execute(Remove_Staff_Query)
                db.commit()
                print("Removed Staff!!")
            except Exception as e:
                print(e)
        elif (superadmin_option == 6):
            print("\n Remove User \n")
            Remove_User_Mobile = input("Enter user mobile number:  ").strip()
            Remove_User_Query = "UPDATE usertable SET status = '{}' WHERE mobile_number = '{}' AND status= '1'".format(
                2, Remove_User_Mobile)
            try:
                cursor.execute(Remove_User_Query)
                db.commit()
                print("Removed User!!")
            except Exception as e:
                print(e)
        elif(superadmin_option==7):
            print("\n Check Status of particular Staff \n")
            staff_mobile = input("Enter Staff Mobile number: ")
            staff_status_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{staff_mobile}';"
            try:
                cursor.execute(staff_status_Query)
                staff_status_data = cursor.fetchall()
                staff_status_UserID = staff_status_data[0][0]
                sta_Query = f"SELECT book_name,book_author,quantity FROM bookrecords WHERE staff_id = '{staff_status_UserID}' AND status = '1';"
                cursor.execute(sta_Query)
                # fetch all rows of data from the SELECT statement
                rows = cursor.fetchall()
                # create a PrettyTable object and set the column names
                table = PrettyTable(['Book Name', 'Book Author', 'Quantity'])
                # iterate through the rows of data and add them to the table
                for row in rows:
                    table.add_row(row)
                # print the table
                print(table)
            except Exception as e:
                print(e)
        elif (superadmin_option == 8):
            print("\n Check Status of particular User \n")
            user_mobile = input("Enter user Mobile number: ")
            user_status_Query = f"SELECT id FROM userTable WHERE mobile_number = '{user_mobile}';"
            try:
                cursor.execute(user_status_Query)
                user_status_data = cursor.fetchall()
                user_status_UserID = user_status_data[0][0]
                user_Query = f"SELECT book_name,book_author,quantity,fine,duedate,bookissuedate FROM bookIssue WHERE userid = '{user_status_UserID}' AND status = '1';"
                cursor.execute(user_Query)
                # fetch all rows of data from the SELECT statement
                rows = cursor.fetchall()
                # create a PrettyTable object and set the column names
                table = PrettyTable(['Book Name', 'Book Author', 'Quantity','Fine', 'Due Date', 'Book Issue Date'])
                # iterate through the rows of data and add them to the table
                for row in rows:
                    table.add_row(row)
                # print the table
                print(table)
            except Exception as e:
                print(e)
        else:
            print("You have enter wrong option")

############################################################################################################

                                            # Staff Section

############################################################################################################


elif (identity_check == 2):
    Staff_login_option = int(input(
        "\t\t\t\t******** First you need to login ******** \n \t1. Login \n \t2. Forgot or Update Password  \n Select : "))
    staffTable = "staffTable"
    if (Staff_login_option == 1):
        print("\t\t\t\t\t******** Login ********")
        list = login(staffTable)
        if (list[0] == "1"):
            status_Query = f"SELECT book_name,book_author,quantity FROM bookrecords where status= '1';"
            try:
                cursor.execute(status_Query)
                # fetch all rows of data from the SELECT statement
                rows = cursor.fetchall()
                # create a PrettyTable object and set the column names
                table = PrettyTable(['Book Name', 'Book Author', 'Quantity'])
                # iterate through the rows of data and add them to the table
                for row in rows:
                    table.add_row(row)
                # print the table
                print(table)
            except Exception as e:
                print(e)
            staff_Option = int(input(
                "\t\tAll of these books are already available in this library.\n\n What would you like to do? You can either add a book, remove a book, or check your status. \n\n 1. Add \n 2. Remove \n 3. Status \n\n Select: "))

            if (staff_Option == 1):
                staffID_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(staffID_Query)
                    staffID_data = cursor.fetchall()
                    # print(list[1])
                    staffID = staffID_data[0][0]
                    # print(staffID)
                    book_Name = input("Enter book name: ").lower().strip()
                    book_Author = input(
                        "Enter book author name: ").lower().strip()
                    book_Quantity = int(input("Enter book Quantity: "))
                    book_category = int(input("Select your book category from these given options: \n \n1. Newspaper\n2.Magzine \n3. Engineering Book \n4. Medical Book \n5. Story Book \n6. Research Paper \n7. Classical Book \n8. Rommance Book \n9. Kids Book \n10. Arts Book \n11. Thrillers Book \n12. Text Books \n13. Finance \n14. Trending Books \n Choose option: "))
                    book_category_name = ""
                    extend = 0
                    if (book_category == 1):
                        book_category_name = "newspaper"
                        extend = 1
                    elif (book_category == 2):
                        book_category_name = "magzine"
                        extend = 5
                    elif (book_category == 3):
                        book_category_name = "enginnering"
                        extend = 30
                    elif (book_category == 4):
                        book_category_name = "medical"
                        extend = 30
                    elif (book_category == 5):
                        book_category_name = "story"
                        extend = 15
                    elif (book_category == 6):
                        book_category_name = "research paper"
                        extend = 3
                    elif (book_category == 7):
                        book_category_name = "classical"
                        extend = 7
                    elif (book_category == 8):
                        book_category_name = "rommance"
                        extend = 7
                    elif (book_category == 9):
                        book_category_name = "kids"
                        extend = 7
                    elif (book_category == 10):
                        book_category_name = "arts"
                        extend = 7
                    elif (book_category == 11):
                        book_category_name = "trillers"
                        extend = 7
                    elif (book_category == 12):
                        book_category_name = "text book"
                        extend = 7
                    elif (book_category == 13):
                        book_category_name = "finance"
                        extend = 15
                    elif (book_category == 14):
                        book_category_name = "trending book"
                        extend = 15
                    else:
                        book_category_name = "Unknown"
                        extend = 5

                    if (book_Quantity < 0):
                        print("You have enter -ve quantity of books.")
                    elif (book_category < 0 and book_category != 0):
                        print("You have enter invalid number.")
                    else:
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
                                book_Records_Querry = "UPDATE bookRecords SET quantity = '{}',category = '{}' WHERE book_name = '{}' AND book_author = '{}' AND status= '1';".format(
                                    book_Quantity+book_records_data2[0][0], book_category_name, book_Name, book_Author)
                                try:
                                    cursor.execute(book_Records_Querry)
                                    # print("Same")
                                    db.commit()
                                except Exception as e:
                                    print(e)
                            else:
                                book_Records_Querry = "INSERT INTO bookRecords(staff_id,book_name,book_author,quantity,category) VALUES('{}','{}','{}','{}','{}');".format(
                                    staffID, book_Name, book_Author, book_Quantity, book_category_name)
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
                Remove_Book_Name = input(
                    "Enter Book Name and Author Name that you want to remove \n1. Book Name: ").lower().strip()
                Remove_Author_Name = input(
                    "2. Book Author Name: ").lower().strip()
                staffID_Query = f"SELECT id FROM staffTable WHERE mobile_number = '{list[1]}';"
                try:
                    # print("1")
                    cursor.execute(staffID_Query)
                    staffID_data = cursor.fetchall()
                    staffID = staffID_data[0][0]
                    # print("2")
                    check_remove_book_query = "SELECT COUNT(book_name) FROM bookRecords WHERE book_name = '{}' AND book_author = '{}' AND staff_id = '{}'".format(
                        Remove_Book_Name, Remove_Author_Name, staffID)
                    try:
                        # print("3")
                        cursor.execute(check_remove_book_query)
                        check_remove_book_query_data = cursor.fetchall()
                        # print(check_remove_book_query_data[0])
                        if (check_remove_book_query_data[0][0] > 0):
                            # print("5")
                            Remove_Book_Query = "UPDATE bookRecords SET status = '{}' WHERE book_name = '{}' AND book_author = '{}' AND staff_id = '{}' AND status= '1'".format(
                                2, Remove_Book_Name, Remove_Author_Name, staffID)
                            try:
                                # print("6")
                                cursor.execute(Remove_Book_Query)
                                db.commit()
                                # print("7")
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)

            elif (staff_Option == 3):
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
                    table = PrettyTable(
                        ['Book Name', 'Book Author', 'Quantity'])
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
        update_Password(staffTable)
    # elif (Staff_login_option == 3):
    #     print("\t\t\t\t******** Create an account ********")
    #     insert(staffTable)
    else:
        print("You have choosen Wrong Input Please try again!!")

elif (identity_check == 3):
    # User Section Code
    User_login_option = int(input(
        "\t\t\t\t########## First you need to login ########## \n \t1. Login \n \t2. Forgot or Update Password \n \t3. Create a Account \n Select : "))
    userTable = "userTable"
    if (User_login_option == 1):
        print("\t\t\t\t\t########## Login ##########")
        list = login(userTable)
        if (list[0] == "1"):
            status_Query = f"SELECT book_name,book_author,quantity FROM bookrecords where status= '1';"
            try:
                cursor.execute(status_Query)
                # fetch all rows of data from the SELECT statement
                rows = cursor.fetchall()
                # create a PrettyTable object and set the column names
                table = PrettyTable(['Book Name', 'Book Author', 'Quantity'])
                # iterate through the rows of data and add them to the table
                for row in rows:
                    table.add_row(row)
                # print the table
                print(table)
            except Exception as e:
                print(e)
            user_Option = int(input(
                "\t\tAll of these books are available in my library.\n\n What would you like to do? You can either issue a book, return a book, or check your status. \n\n 1. Book Issue \n 2. Return Book \n 3. Status of your account \n\n Select: "))
            if (user_Option == 1):
                user_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(user_Query)
                    user_data = cursor.fetchall()
                    userID = user_data[0][0]
                    book_Name = input("Enter book name: ").lower().strip()
                    book_Author = input(
                        "Enter book author name: ").lower().strip()
                    book_Quantity = int(input("Enter book Quantity: "))
                    if (book_Quantity < 0):
                        print("You have enter -ve quantity of book")
                    elif (book_Quantity == 0):
                        print("You have entered Zero quantity of book.")
                    elif (book_Quantity == 1):
                        book_Issue_Check_Querry1 = "SELECT book_name, book_author, quantity,category FROM bookRecords WHERE book_name = '{}' AND book_author = '{}';".format(
                            book_Name, book_Author)
                        book_Issue_Check_Querry2 = "SELECT COUNT(book_name) FROM bookIssue WHERE book_name = '{}' AND book_author = '{}' AND userid = '{}';".format(
                            book_Name, book_Author, userID)
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
                            # print("1")

                            if (cursor.fetchone() is not None):
                                # print("2")
                                if (book_Issue_data1[0][0] == book_Name and book_Issue_data1[0][1] == book_Author):
                                    # print("3")
                                    if ((int(book_Quantity)) <= book_Issue_data1[0][2]):
                                        # print("4")
                                        if (book_Issue_data2[0][0] > 0):
                                            if ((int(book_Quantity) + int(book_Issue_data3[0][0]) <= book_Issue_data1[0][2])):
                                                # print("5")
                                                book_category = book_Issue_data1[0][3]
                                                extend = 0
                                                if (book_category == "newspaper"):
                                                    extend = 1
                                                elif (book_category == "magzine"):
                                                    extend = 5
                                                elif (book_category == "enginnering"):
                                                    extend = 30
                                                elif (book_category == "medical"):
                                                    extend = 30
                                                elif (book_category == "story"):
                                                    extend = 15
                                                elif (book_category == "research paper"):
                                                    extend = 3
                                                elif (book_category == "classical"):
                                                    extend = 7
                                                elif (book_category == "rommance"):
                                                    extend = 7
                                                elif (book_category == "kids"):
                                                    extend = 7
                                                elif (book_category == "arts"):
                                                    extend = 7
                                                elif (book_category == "trillers"):
                                                    extend = 7
                                                elif (book_category == "text book"):
                                                    extend = 7
                                                elif (book_category == "finance"):
                                                    extend = 15
                                                elif (book_category == "trending book"):
                                                    extend = 15
                                                else:
                                                    extend = 5

                                                book_Issue_Querry = "UPDATE bookIssue SET quantity = '1', status = '1' WHERE book_name = '{}' AND book_author = '{}' AND userid = '{}' AND status= '2';".format(
                                                    book_Name, book_Author, userID)
                                                try:
                                                    cursor.execute(
                                                        book_Issue_Querry)
                                                    db.commit()
                                                    book_Issue_Date = "SELECT bookissuedate FROM bookIssue WHERE book_name = '{}' AND book_author = '{}' AND status= '1' AND userid = '{}';".format(
                                                        book_Name, book_Author, userID)
                                                    try:
                                                        # print("1")
                                                        cursor.execute(
                                                            book_Issue_Date)
                                                        # print("2")
                                                        book_Issue_Date_Data = cursor.fetchall()
                                                        # print("3")
                                                        book_Due_Date = add_due_date(
                                                            book_Issue_Date_Data[0][0].strftime('%Y/%m/%d'), extend)
                                                        # print("4")
                                                        book_Due = "Update bookIssue SET duedate = '{}' Where book_name = '{}' AND book_author = '{}' AND status= '1' AND userid = '{}';".format(
                                                            book_Due_Date, book_Name, book_Author, userID)
                                                        try:
                                                            # print("5")
                                                            cursor.execute(
                                                                book_Due)
                                                            # print("6")
                                                            db.commit()
                                                            # print("7")
                                                        except Exception as e:
                                                            print(e)
                                                    except Exception as e:
                                                        print(e)
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

                                                except Exception as e:
                                                    print(e)
                                            else:
                                                print(
                                                    "That quantity of books are not available to this library please search on other library.")

                                        else:
                                            # print("6")
                                            book_Issue_Querry = "INSERT INTO bookIssue(userid,book_name,book_author,quantity) VALUES('{}','{}','{}','{}');".format(
                                                userID, book_Name, book_Author, book_Quantity)
                                            try:
                                                # print("7")
                                                cursor.execute(
                                                    book_Issue_Querry)
                                                db.commit()
                                                
                                                book_category = book_Issue_data1[0][3]
                                                extend = 0
                                                if (book_category == "newspaper"):
                                                    extend = 1
                                                elif (book_category == "magzine"):
                                                    extend = 5
                                                elif (book_category == "enginnering"):
                                                    extend = 30
                                                elif (book_category == "medical"):
                                                    extend = 30
                                                elif (book_category == "story"):
                                                    extend = 15
                                                elif (book_category == "research paper"):
                                                    extend = 3
                                                elif (book_category == "classical"):
                                                    extend = 7
                                                elif (book_category == "rommance"):
                                                    extend = 7
                                                elif (book_category == "kids"):
                                                    extend = 7
                                                elif (book_category == "arts"):
                                                    extend = 7
                                                elif (book_category == "trillers"):
                                                    extend = 7
                                                elif (book_category == "text book"):
                                                    extend = 7
                                                elif (book_category == "finance"):
                                                    extend = 15
                                                elif (book_category == "trending book"):
                                                    extend = 15
                                                else:
                                                    extend = 5

                                                book_Issue_Date = "SELECT bookissuedate FROM bookIssue WHERE book_name = '{}' AND book_author = '{}' AND status= '1' AND userid = '{}';".format(
                                                    book_Name, book_Author, userID)
                                                try:
                                                    print("1")
                                                    cursor.execute(
                                                        book_Issue_Date)
                                                    print("2")
                                                    book_Issue_Date_Data = cursor.fetchall()
                                                    print("3")
                                                    book_Due_Date = add_due_date(
                                                        book_Issue_Date_Data[0][0].strftime('%Y/%m/%d'), extend)
                                                    print("4")
                                                    book_Due = "Update bookIssue SET duedate = '{}' Where book_name = '{}' AND book_author = '{}' AND status= '1' AND userid = '{}';".format(
                                                        book_Due_Date, book_Name, book_Author, userID)
                                                    try:
                                                        print("5")
                                                        cursor.execute(
                                                            book_Due)
                                                        print("6")
                                                        db.commit()
                                                        print("7")
                                                    except Exception as e:
                                                        print(e)
                                                except Exception as e:
                                                    print(e)
                                            except Exception as e:
                                                print(e)
                                    else:
                                        print(
                                            "That quantity of books are not available to this library please search on other library.")
                            else:
                                print(
                                    "This book are not available in my library please search on other library.")
                        except Exception as e:
                            print(e)
                    else:
                        print("You have only permission to issue a single book")
                except Exception as e:
                    print(e)
            elif (user_Option == 2):
                user_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(user_Query)
                    user_data = cursor.fetchall()
                    userID = user_data[0][0]
                    book_Name = input("Enter book name: ").lower().strip()
                    book_Author = input(
                        "Enter book author name: ").lower().strip()
                    book_Quantity = int(input("Enter book Quantity: "))
                    if (book_Quantity == 1):
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
                                            book_Issue_Querry = "UPDATE bookIssue SET quantity = '{}',status = '2' WHERE book_name = '{}' AND book_author = '{}';".format(
                                                int(book_Issue_data3[0][0]) - int(book_Quantity), book_Name, book_Author)
                                            try:
                                                cursor.execute(
                                                    book_Issue_Querry)
                                                db.commit()
                                            except Exception as e:
                                                print(e)
                                    else:
                                        print(
                                            "That quantity of books are not from this library please return this book to other library.")
                            else:
                                print(
                                    "This book are not from this library please go on other library.")
                        except Exception as e:
                            print(e)
                    else:
                        print(
                            "You have only permit to issue a single book or return a single book only.")
                except Exception as e:
                    print(e)
            elif (user_Option == 3):
                status_Query = f"SELECT id FROM userTable WHERE mobile_number = '{list[1]}';"
                try:
                    cursor.execute(status_Query)
                    status_data = cursor.fetchall()
                    status_UserID = status_data[0][0]
                    sta_Query = f"SELECT book_name,book_author,quantity,fine,duedate,bookissuedate FROM bookIssue WHERE userid = '{status_UserID}' AND status = '1';"
                    cursor.execute(sta_Query)
                    # fetch all rows of data from the SELECT statement
                    rows = cursor.fetchall()
                    # create a PrettyTable object and set the column names
                    table = PrettyTable(
                        ['Book Name', 'Book Author', 'Quantity', 'Fine', 'Due Date', 'Book Issue Date'])
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
        update_Password(userTable)
    elif (User_login_option == 3):
        print("\t\t\t\t########## Create an account ##########")
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
# ALTER TABLE superadmin OWNER TO ujjawal;
# ALTER TABLE usertable OWNER TO ujjawal;
# UPDATE bookrecords SET book_name = 'python crash course' WHERE bookid = 1 RETURNING *;
# Alter table bookrecords ALTER COLUMN quantity TYPE INTEGER USING quantity::integer;
# ALTER TABLE bookrecords DROP COLUMN staff_id;
# ALTER TABLE bookreturn ADD PRIMARY KEY (id);
# ALTER TABLE bookreturn ADD COLUMN id SERIAL;
# CREATE TABLE superadmin(id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL,last_name VARCHAR(100) NOT NULL,mobile_number varchar(15) UNIQUE,email_id varchar(100) UNIQUE,password varchar(100));
# ALTER TABLE superadmin ADD COLUMN date_of_birth varchar(10);