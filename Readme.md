<img src="https://komarev.com/ghpvc/?username=ayeujjawalsingh&label=Profile%20Visiters&color=0e75b6&style=flat" alt="ayeujjawalsingh" />

<h1 align="center"> Hey 👋🏻, I'm Ujjawal Singh </br> 
</h1>
<p align="center">Software Developer || Full Stack Developer || Data Analyst</p>
<p align="center">
<a href="https://auth.geeksforgeeks.org/user/ayeujjawalsingh/practice" target="_blank"><img alt="" src="https://img.shields.io/badge/GeeksforGeeks-000?logo=GeeksforGeeks&logoColor=2FF200&style=for-the-badge" style="vertical-align:center" /></a>
<a href="https://linkedin.com/in/ayeujjawalsingh" target="_blank"><img alt="" src="https://img.shields.io/badge/LinkedIn-000?logo=linkedin&logoColor=0A66C2&style=for-the-badge" style="vertical-align:center" /></a>
<a href="https://github.com/ayeujjawalsingh" target="_blank"><img alt="" src="https://img.shields.io/badge/Github-000?logo=github&logoColor=f4f9fe&style=for-the-badge" style="vertical-align:center" /></a>
<a href="https://leetcode.com/ayeujjawalsingh/" target="_blank"><img alt="" src="https://img.shields.io/badge/Leetcode-000?logo=leetcode&logoColor=FFF926&style=for-the-badge" style="vertical-align:center" /></a></p>
<hr>
<h2 align="center">Description of Library Management System</h2>

<p>
In this project has three interfaces - one for the superuser, one for the staff, and another for the users. The purpose of the system is to enable all the operations performed in a physical library to be performed in a virtual environment. The system is written in Python and uses PostgreSQL for database operations.

I have used the ARGON2 hashing technique to store passwords in an encrypted format, which is a good security measure to protect user data. This ensures that even if someone gains access to the database, they will not be able to read the passwords in plain text format.

The superadmin account is the most powerful account in the system, and it can perform all the operations that are possible for both the staff and the users. Only the data administrator can create a superadmin account, ensuring that this level of access is given only to trusted individuals.

The staff ID can only be created by the superadmin, and they have the power to add or remove books from the library. This ensures that the library's inventory is always up-to-date and accurate.

Users can create their own accounts, or they can be created by the superadmin, giving them access to the system.

The users have the ability to update their account information and reset their passwords if they forget them. This ensures that users can always access their accounts and their borrowed books without any issues.

Users can borrow books from the library and then return them within a certain due date. If they fail to return the book on time, they will be charged a fine based on the book's category and the number of days overdue. This encourages users to return the books on time, and it also helps the library maintain its inventory.
</p>
<!-- <hr> -->

<!-- <p>
In this Library Management System project, I have implemented a login system with three user types: super admin, staff, and user.
</p> -->

## 1. Super Admin Section

<p>
When logged in as a super admin, the system displays a menu with seven options.

1. Add Staff: This option allows the super admin to add a new staff member to the system. The super admin can enter the staff member's details, such as name, email, and password.
 
2. Add User: This option allows the super admin to add a new user to the system. The super admin can enter the user's details, such as name, email, and password.
 
3. Add Book: This option allows the super admin to add a new book to the library. The super admin can enter details about the book, such as the title, author.
 
4. Remove Book: This option allows the Super Admin to remove a book from the library. The Super Admin can search for a book by its title or ISBN and remove it from the system.
 
5. Remove Staff: This option allows the super admin to remove a staff member from the system. The super admin can search for the staff member by name or email and remove them from the system.
 
6. Remove User: This option allows the super admin to remove a user from the system. The super admin can search for the user by name or email and remove them from the system.
 
7. Check Status of Particular Staff: This option allows the super admin to check the status of a particular staff member. The super admin can search for the staff member by their mobile number and check their status in the system.
 
8. Check Status of Particular User: This option allows the super admin to check the status of a particular user. The super admin can search for the user by their mobile number and check their status in the system.
</p>

## 2. Staff Section

<p>
When logged in as a staff member, the system displays a menu with three options.

1. Add: This option allows the staff member to add a new book to the library. The staff member can enter details about the book, such as the title, author name, and quantity of the book.
 
2. Remove: This option allows the staff member to remove a book from the library. The staff member can search for a book by its title and remove it from the system.
 
3. Status: This option allows the staff member to check their status in the system, such as the number of books they have added.
</p>

## 3. User Section

<p>
When logged in as a user, the system displays a menu with three options.

1. Book Issue: This option allows the user to issue a book from the library. The user can search for a book by its title and author name and issue it for a certain period.
 
2. Return Book: This option allows the user to return a book to the library. The user can search for a book by its title and author name and return it to the library.
 
3. Status: This option allows the user to check their status in the system, such as the number of books they have issued, returned, and fined.
</p>
