## Web Application Project

Waikirikiri Library web application project is specially designed for the ‘Public’ (that is Readers who get books issued) and ‘Staff Members‘ of the Library who has the access of performing actions on the borrowers(search, updation of the details, add borrowers, issue and return books and generate reports for the loans issued). This project is a live web app on PythonAnywhere which is further connected to Github for data updation.

We have been given the web app project in which we had to make two interfaces

## Public- 
This interface is mainly for the borrowers who can search the books available and see the list of books with the availability and due date. The requirement of the project is to access this route by “/“.
## Staff- 
This interface is maily for the staff of the library to perform actions and the requirement of the project to access this route is “/staff“.
I used Python, Flask, Mysql and Jinja+css codes to build the interface and apply routes within the interfaces and get the operations done for the given requirement.

## Staff Login - 
* Password - Staff123

## Outline of the routes and functions:

For Flask web app, there is requirement of ‘App.py’ file which is a python flask file, used to make interfaces and programming is performed with the help of mysql queries. Along with this, templates (HTML, Jinjs, CSS) are required for the validation purposes, fetching data for website, coding of it. ‘Connect.py’ is a connection file which links the database tp the flask app to perform actions the database of the library. For this, certain number of routes and functions are required to build so that users would be able to perform actions and navigate through the website.

For Public interface, the requirement is to make it accessible by “/“ route, and this interface has two nav bar items, one is ‘Search Books’ and other is ‘List Books’. This interface is linked with ‘base.html’ page which has CSS Bootstrap coding for the good UI and for making options available on the nav bar for navigating from one section to another.
"@app.route("/")
def home():"
function ‘home()’ is assigned with decorater- indicating that it is the homepage of the website
A. Search books- This bar item allows the borrower/user to search the book.

@app.route("/booksearches", methods=["GET"])
def public():  
return render_template("booksearch.html")
This has function named ‘public():’ which renders the template ‘booksearch.html’ which has the required form fields to search. The requirement for the search books is to allow the public to search the books either by Title or Author having partial search access so that user should not get problem in getting the exact word/title or author of the book. In Booksearch.html template, two fields are provided having validation check, which helps the public in retrieving the information about list of books available. When the user does any search, it gets redirected to ‘booklist1.html’, which shows the books information which are searched and for this, ‘POST’ method is used having function ‘booksearches():’.
Assumptions and Design Decisions:

Design Decision assumptions= Both public and staff would be able to login in the website as in the case of borrower, he would be able to see the previous loans and staff would be able to have their privacy according to policy as any unauthorized staffm member could also access the information.

Loan Summary report- Assumption= While determining the loan count of the loans taken, two assumptions could be made as

select bc.bookcopyid,bc.bookid, bc.format,COUNT(l.bookcopyid) AS loan_count
from bookcopies bc
LEFT JOIN loans l on bc.bookcopyi= l.bookcopyid
group by bc.bookcopyid;
Loan count per bookcopy could be used to get the loan count per book copy
However, if it is to be grouped by book, then it could be done by how many times books have been borrowed by the borrower.

BorrowerID assumption- Borrowerid could be made hidden whenever a loan is returned as loanid could also help in retrieving the information, the list of borrowers could also have borrowerid hidden as ID could be a unique identifier for the user, but if we consider the case for book issue it will be helpful.
B. List Books: It shows the list of available books to the public with the availability of the books and due date so that when it could be borrowed, can be known.

@app.route("/listbooks", methods=["GET"])
def listbooks():
“/listbooks” is the route for the public to get access to the list of available books and uses “GET” method to retrieve the data. “listbooks():” function processses the sql query and renders the “booklist.html” template to show the content with format, availability and due date.

For Staff interface:
@app.route("/staff")
def staff():
return render_template("staff1.html")
“/staff” interface is accessed which has “staff()” function, which renders “staff1.html” page having the navigation bars.
A. Search Books: @app.route(“/staff/booksearches”, methods=[“GET”])
def staffbooksearch():
return render_template("booksearchstaff.html")
“/staff/booksearches” route is used to perform search action by the staff using GET method which requests data from the form by “staffbooksearch():” function which renders “booksearchstaff.html” template and propmts the user to enter the data for search.
@app.route("/staff/booksearches", methods=["POST"])
def staffbooksearches():
This is the same route in staff interface but having method “POST”, which means “staffbooksearches():” function runs the queries which are in “if-elif” form according to the user input, which further renders the “booklist2.html” template and displays data.

B. List Books:

@app.route("/staff/listbooks", methods=["GET"])
def listbooks1():
“/staff/listbooks” route is used to access the list of books by the staff and GET method is used as the user tries to retrieve data from the source that is “booklist.html” template, which is rendered and shows the result of books with their format, availability and due date. Function “listbooks1()” is used.
C. Borrowers:

Search Borrower:
@app.route("/staff/borrowerdetails", methods=["GET"])
def staffborrowerdetails():
return render_template("borrowerdetails.html")
To search the borrower, staff member when clicks on the Search the borrower tab, “/staff/borrowerdetails” route is accessed, which has GET method to fetch the details from the “borrowerdetails.html”.
@app.route("/borrowerdetails", methods=["POST"])
def borrowerdetails():
Upon clicking on search button, staff member gets redirected to “/borrowerdetails” route which renders the “Borrowerlist.html” template by using the POST method as data is sent to the borrowerlist.
Add borrower:
@app.route("/staff/addborrower")
def staffaddborrower():
return render_template("addborrower.html")
This route renders addborrower.html and prompts the user to fill the form.
@app.route("/staff/addborrower", methods=["POST"])  
def addborrower():
Upon clicking Add borrower tab, user will be redirected to “/staff/addborrower” route, which renders addborrower.html template using GET method and once the user, fills up the information of the borrower and clicks on submit button, it gets added to the list of borrowers using POST method as data is sent to the source and redirects the user to the borrowers list.

Edit and Update Borrower: edit the borrower: ```python
@app.route("/editborrower/<int:borrowerid>", methods=["GET", "POST"])
def editborrower(borrowerid):
if request.method == "GET":
When a borrower is being searched using search function, list of borrowers appears and if the staff member wants to edit the user, this route is accessed in which borrowerid is called and passed to the function “editborrower():” Uses GET method for requesting data and POST for sending. It renders “edit.html” template.

@app.route("/updateborrower", methods=["GET", "POST"])
def updateborrower():
if request.method == "POST":
When user clicks on Update button after editing the details, “/updateborrower” route is accessed which uses POST method to send the data to the List of Borrowers and gets the data updated.

Issue book to a borrower:
@app.route("/staff/issuebook", methods=["GET"])
def bookissue():
Book or Loan issue option is under the Loans dropdown and when the staff member has to issue any book to the public, one clicks on Issue and gets redirected to this “/staff/issuebook” route, from where the data is rendered through issuebook.html template using GET method. Bookissue() function is defined.
@app.route("/bookissued", methods=["GET", "POST"])
def bookissued():
When the bookcopyid and borrowerid is selected from the data fetched from issuebook.html, after submitting, user gets redirected to the “/bookissued” route which displays the currentloans page showing which books are on loan and returned as well using both GET and POST method.

5.Return Books:

@app.route("/editloan/<int:bookcopyid>", methods=["GET", "POST"]) def editloan(bookcopyid):
When user clicks on the Loans dropdown and clicks Return button, currentloans page gets opened with Edit button. When user clicks on edit, user gets redirected to this above route for edit loan which uses both GET and POST method and bookcopyid is passed through the funtion editloan().

@app.route("/updatebookstatus", methods=["GET", "POST"])
def bookreturn():
When the status of the book is changed from ‘onloan’ to ‘returned’, and clicks on update, the “/updatebookstatus” route is accessed, which then redirects the user to the currentloans page and update the loan status there by using POST method.

Overdue Books report:
@app.route("/staff/overduebooks", methods=["GET"])
def overduebooks():
When staff member on the webpage clicks on dropdown, a menu opens and when “overdue loans” appear on the screen , then “/staff/overduebooks” route is used to retrieve the loans which are overdue in the form of “overdue Days”. GET method is used and overduebooks(): is used to access the query to get the result from the source and this renders “overduebookreport.html” template to get the results in the form of table. 7.** Loan Summary report:**

@app.route("/staff/loansummary", methods=["GET"])
def loansummary():
From the same nav bar dropdown menu, when the staff member clicks on “Loan Summary”, “/staff/loansummary” route is accessed to retrieve the loans summary that is the loan count of the books being borrowed. “GET” method is used to request data and “loansummary():” function runs the query to provide the loan count by rendering “loansummary.html” template.

8.Borrower Summary report:

@app.route("/staff/borrowersummary", methods=["GET"])
def borrowersummary():
This route also uses GET method to get the data of the borrowers’ past and current loan count. “/staff/borrowersummary” route is accessed upon clicking on Borrower Summary under loans dropdown. “Borrowersummary():” function is defined, which is used to run the query and renders “borrowersummary.html” template to display the result.
Assumptions and Design Decisions:

Design Decision assumptions= Both public and staff would be able to login in the website as in the case of borrower, he would be able to see the previous loans and staff would be able to have their privacy according to policy as any unauthorized staffm member could also access the information.

Loan Summary report- Assumption= While determining the loan count of the loans taken, two assumptions could be made as

select bc.bookcopyid,bc.bookid, bc.format,COUNT(l.bookcopyid) AS loan_count
from bookcopies bc
LEFT JOIN loans l on bc.bookcopyi= l.bookcopyid
group by bc.bookcopyid;
Loan count per bookcopy could be used to get the loan count per book copy
However, if it is to be grouped by book, then it could be done by how many times books have been borrowed by the borrower.

BorrowerID assumption- Borrowerid could be made hidden whenever a loan is returned as loanid could also help in retrieving the information, the list of borrowers could also have borrowerid hidden as ID could be a unique identifier for the user, but if we consider the case for book issue it will be helpful.
Add loan and issue book - Assumed to be same as both works in the same way both has same query functions to run.
