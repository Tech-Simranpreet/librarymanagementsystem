from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None


def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=True,
    )
    dbconn = connection.cursor()
    return dbconn


# route for public for homepage
# @app.route("/")
# def home1():
#     return "Hello, Flask!"


@app.route("/")
def home():
    return render_template("base.html")  # renders base.html template


# route for staff to access staff homepage, renders staff1.html page which has fields for performing certain actions.


@app.route("/staff")
def staff():
    return render_template("staff1.html")


# route for redirecting to booksearch.html and performing search action by the public.


# GET method is used to fetch the fields.
@app.route("/booksearches", methods=["GET"])
def public():
    return render_template("booksearch.html")


# staff book search route
# renders booksearchstaff.html template
# GET method is used to request data from the specified file.
# staffbooksearch() function as a defined decorator.


@app.route("/staff/booksearches", methods=["GET"])
def staffbooksearch():
    return render_template("booksearchstaff.html")


# route to search the borrower
# requests data by rendering borrowerdetails.html using GET method


@app.route("/staff/borrowerdetails", methods=["GET"])
def staffborrowerdetails():
    return render_template("borrowerdetails.html")


# route for staff to add borrower
# form is rendered for filing new borrower's details.
# GET method is used.
@app.route("/staff/addborrower")
def staffaddborrower():
    return render_template("addborrower.html")


# route for the staff to issue book
# GET method is used to request data from issuebook.html


@app.route("/staff/issuebook", methods=["GET"])
def bookissue():
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies
inner join books on books.bookid = bookcopies.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1 or returned is NULL);"""
    connection.execute(sql)
    bookList = connection.fetchall()
    return render_template("issuebook.html", books=bookList, borrowers=borrowerList)


# bookissued route for the staff
# book is issued on loan and displays on currentloans page.
# uses both GET and POST method.


@app.route("/bookissued", methods=["GET", "POST"])
def bookissued():

    borrowerid = request.form.get("borrower")
    bookid = request.form.get("book")
    # loandate = request.form.get('loandate')
    from datetime import datetime

    loandate = datetime.now().strftime("%Y-%m-%d")
    print(loandate)
    cur = getCursor()
    cur.execute(
        "INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",
        (
            borrowerid,
            bookid,
            str(loandate),
        ),
    )
    return redirect("/currentloans")


# route to display the list of books for public
# GET method is used to retrieve the data of the books available


@app.route("/listbooks", methods=["GET"])
def listbooks():
    connection = getCursor()
    sql = """select bk.booktitle, bk.author, bk.category, bk.yearofpublication, bc.format,
CASE when returned = 1 THEN 'Available'
ELSE 'Not Available' END as Availability,
case when date_add(loandate, interval 28 day)>NOW() THEN date_add(loandate, interval 28 day)
else "" end as due_date
from books bk
inner join bookcopies bc ON bk.bookid = bc.bookid
inner join loans l ON bc.bookcopyid = l.bookcopyid;"""
    connection.execute(sql)
    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist.html", booklist=bookList)


# route for staff to get the list of books
# uses GET method to request data from booklist
# shows availability of books with due date and format.


@app.route("/staff/listbooks", methods=["GET"])
def listbooks1():
    connection = getCursor()
    sql = """select bk.booktitle, bk.author, bk.category, bk.yearofpublication, bc.format,
CASE when returned = 1 THEN 'Available'
ELSE 'Not Available' END as Availability,
case when date_add(loandate, interval 28 day)>NOW() THEN date_add(loandate, interval 28 day)
else "" end as due_date
from books bk
inner join bookcopies bc ON bk.bookid = bc.bookid
inner join loans l ON bc.bookcopyid = l.bookcopyid;"""
    connection.execute(sql)
    bookList = connection.fetchall()
    print(bookList)

    return render_template("booklist.html", booklist=bookList)


# route to display the loans
# renders addloan.html template by GET method


@app.route("/loanbook")
def loanbook():
    todaydate = datetime.now().date()
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    sql = """SELECT * FROM bookcopies
inner join books on books.bookid = bookcopies.bookid
 WHERE bookcopyid not in (SELECT bookcopyid from loans where returned <> 1 or returned is NULL);"""
    connection.execute(sql)
    bookList = connection.fetchall()
    return render_template(
        "addloan.html", loandate=todaydate, borrowers=borrowerList, books=bookList
    )


# route for adding the loan
# displays the list of books onloan
# POST method is used


@app.route("/loan/add", methods=["POST"])
def addloan():
    borrowerid = request.form.get("borrower")
    bookid = request.form.get("book")
    loandate = request.form.get("loandate")
    cur = getCursor()
    cur.execute(
        "INSERT INTO loans (borrowerid, bookcopyid, loandate, returned) VALUES(%s,%s,%s,0);",
        (
            borrowerid,
            bookid,
            str(loandate),
        ),
    )
    return redirect("/currentloans")


# Route to list the borrowers list
# renders borrowerlist.html
# borrowerList is the variable passed to borrowerlist


@app.route("/listborrowers", methods=["GET"])
def listborrowers():
    connection = getCursor()
    connection.execute("SELECT * FROM borrowers;")
    borrowerList = connection.fetchall()
    return render_template("borrowerlist.html", borrowerlist=borrowerList)


# route to display the loans currently taken by the borrowers
# loanList the variable passed to loanlist


@app.route("/currentloans")
def currentloans():
    connection = getCursor()
    sql = """ select br.borrowerid, br.firstname, br.familyname,  
                l.borrowerid, l.bookcopyid, l.loandate, l.returned, b.bookid, b.booktitle, b.author, 
                b.category, b.yearofpublication, bc.format 
            from books b
                inner join bookcopies bc on b.bookid = bc.bookid
                    inner join loans l on bc.bookcopyid = l.bookcopyid
                        inner join borrowers br on l.borrowerid = br.borrowerid
            order by br.familyname, br.firstname, l.loandate;"""
    connection.execute(sql)
    loanList = connection.fetchall()
    return render_template("currentloans.html", loanlist=loanList)


# route for searching book for the public
# POST method is used to search the book as the data is sent by search form
# booklist1.html template is rendered


@app.route("/booksearches", methods=["POST"])
def booksearches():
    title = request.form["title"]
    author = request.form["author"]
    # if-elif statement used to get the desired search results
    connection = getCursor()
    if title != "" and author != "":
        _title = "%" + title + "%"
        _author = "%" + author + "%"

        connection.execute(
            "SELECT * FROM books WHERE booktitle LIKE %s OR author LIKE %s;",
            (
                _title,
                _author,
            ),
        )

    elif title != "" and author == "":
        _title = "%" + title + "%"
        connection.execute("SELECT * FROM books WHERE booktitle LIKE %s;", (_title,))

    elif title == "" and author != "":
        _author = "%" + author + "%"
        connection.execute("SELECT * FROM books WHERE author LIKE %s;", (_author,))

    bookList = connection.fetchall()
    print(bookList)
    return render_template("booklist1.html", booklist=bookList)


# route for staff book search
# POST method to send data to the booklist2.html template


@app.route("/staff/booksearches", methods=["POST"])
def staffbooksearches():
    title = request.form["title"]
    author = request.form["author"]

    # if-elif statement used for retrieving data according to input.
    connection = getCursor()
    if title != "" and author != "":
        _title = "%" + title + "%"
        _author = "%" + author + "%"
        connection.execute(
            "SELECT * FROM books WHERE booktitle LIKE %s OR author LIKE %s;",
            (
                _title,
                _author,
            ),
        )

    elif title != "" and author == "":
        _title = "%" + title + "%"
        connection.execute("SELECT * FROM books WHERE booktitle LIKE %s;", (_title,))

    elif title == "" and author != "":
        _author = "%" + author + "%"
        connection.execute("SELECT * FROM books WHERE author LIKE %s;", (_author,))

    bookList = connection.fetchall()
    print(bookList)
    return redirect("booklist2.html", booklist=bookList)


# route for staff to search borrowers
# POST method is used to send data
@app.route("/borrowerdetails", methods=["POST"])
def borrowerdetails():  # fucntion defined
    # if-elif-else statement used to get search result
    search = request.form["Search"]
    value = request.form["value"]
    connection = getCursor()
    if search == "BorrowerName":
        searchborrower = "%" + value + "%"
        connection.execute(
            "Select * from borrowers WHERE familyname LIKE %s;", (searchborrower,)
        )
    elif search == "BorrowerID":
        searchborrower = "%" + value + "%"
        connection.execute(
            "Select * from borrowers WHERE borrowerid LIKE %s;", (searchborrower,)
        )
    else:
        connection.execute("Select * from borrowers;")

    borrowerList = connection.fetchall()
    print(borrowerList)
    return render_template("borrowerlist.html", borrowerlist=borrowerList)


# route for staff to add borrower
# POST method is used to send data to borrowers list
# List of borrowers is shown after adding borrower
@app.route("/staff/addborrower", methods=["POST"])
def addborrower():
    borrowerid = request.form.get("borrower")
    firstname = request.form.get("firstname")
    familyname = request.form.get("familyname")
    dateofbirth = request.form.get("dateofbirth")
    housenumbername = request.form.get("housenumbername")
    street = request.form.get("street")
    town = request.form.get("town")
    city = request.form.get("city")
    postalcode = request.form.get("postalcode")
    cur = getCursor()
    # insert query to add borrower in borrowers table
    cur.execute(
        "INSERT into borrowers (borrowerid, firstname, familyname, dateofbirth, housenumbername, street, town, city, postalcode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        (
            borrowerid,
            firstname,
            familyname,
            dateofbirth,
            housenumbername,
            street,
            town,
            city,
            postalcode,
        ),
    )
    return redirect("/listborrowers")


# route for editing the existing borrower from borrowerdetails
# uses GET method to request data from the page
# borrowerid is passed to the function
@app.route("/editborrower/<int:borrowerid>", methods=["GET", "POST"])
def editborrower(borrowerid):
    if request.method == "GET":
        connection = getCursor()
        connection.execute(
            "Select * from borrowers WHERE borrowerid = %s;", (borrowerid,)
        )
        borrowerList = connection.fetchone()
        print(borrowerList)
        return render_template("edit.html", borrowerlist=borrowerList)


# route to update borrower by staff
# POST method is used to update data to the list of borrowers.
# redirects tge user to /listborrowers
@app.route("/updateborrower", methods=["GET", "POST"])
def updateborrower():
    if request.method == "POST":

        firstname = request.form["firstname"]
        borrowerid = int(request.form["id"])
        familyname = request.form["familyname"]
        dateofbirth = request.form["dateofbirth"]
        housenumbername = request.form["housenumbername"]
        street = request.form["street"]
        town = request.form["town"]
        city = request.form["city"]
        postalcode = request.form["postalcode"]
        cur = getCursor()
        cur.execute(
            "UPDATE borrowers SET firstname = %s, familyname = %s, dateofbirth = %s, housenumbername = %s, street = %s, town = %s, city = %s, postalcode = %s WHERE (borrowerid = %s);",
            (
                firstname,
                familyname,
                dateofbirth,
                housenumbername,
                street,
                town,
                city,
                postalcode,
                borrowerid,
            ),
        )
        connection.commit()
        return redirect("/listborrowers")


# route to return loan
# edit available through currentloans
# bookcopyid is passed to the function
# uses GET to request the status


@app.route("/editloan/<int:bookcopyid>", methods=["GET", "POST"])
def editloan(bookcopyid):
    if request.method == "GET":
        connection = getCursor()
        connection.execute("Select * from loans WHERE bookcopyid = %s;", (bookcopyid,))
        loanList = connection.fetchone()
        print(loanList)
        return render_template("editloan.html", loanlist=loanList)


# book status is updated
# this route redirects the user to currentloans page
# POST method is used to get send data as status update to currentloans.


@app.route("/updatebookstatus", methods=["GET", "POST"])
def bookreturn():
    if request.method == "POST":
        loan = int(request.form["id"])
        returned = request.form["returned"]
    cur = getCursor()
    cur.execute("update loans set returned = %s WHERE loanid = %s;", (returned, loan))
    connection.commit()
    return redirect("/currentloans")


# Overdue Books report
# staff has access of overduebooks
# GET method is used to request data with overduebooks()


@app.route("/staff/overduebooks", methods=["GET"])
def overduebooks():
    # sql query is passed to the connection.execute
    connection = getCursor()
    sql = """SELECT books.bookid, books.booktitle, borrowers.borrowerid, borrowers.fullname, bookcopies.format, DATEDIFF(NOW(), loans.loandate) AS daysoverdue from books

                INNER JOIN 

                bookcopies on books.bookid = bookcopies.bookid

                INNER JOIN 

                loans on bookcopies.bookcopyid = loans.bookcopyid 

                INNER JOIN

                borrowers on loans.borrowerid = borrowers.borrowerid

                WHERE DATEDIFF(NOW(), loans.loandate) >  35;"""
    connection.execute(sql)
    # renders overduebookreport template
    return render_template("overduebookreport.html", books=connection.fetchall())


# loan summary of the borrowed books
# GET method is used to get loan summary by defining function loansummary()


@app.route("/staff/loansummary", methods=["GET"])
def loansummary():
    connection = getCursor()
    sql = """select b.booktitle, b.author, b.category, COUNT(bookcopies.bookid) as borrowed_times from books b
        INNER JOIN bookcopies ON b.bookid = bookcopies.bookid
        INNER JOIN loans ON loans.bookcopyid = bookcopies.bookcopyid
        GROUP BY  b.bookid; """
    connection.execute(sql)
    # renders loansummary.html template
    return render_template("loansummary.html", books=connection.fetchall())


# Borrowers past and current loan count displays with this report
# Used method is GET


@app.route("/staff/borrowersummary", methods=["GET"])
def borrowersummary():
    # runs sql query Group By clause is used to group borrower's ids.
    connection = getCursor()
    sql = """select br.borrowerid, br.firstname, br.familyname, br.dateofbirth, COUNT(l.borrowerid) AS loan_count   
        from borrowers br
            LEFT JOIN loans l on br.borrowerid = l.borrowerid
        GROUP BY br.borrowerid;"""
    connection.execute(sql)
    # renders borrowersummary.html
    return render_template("borrowersummary.html", borrowers=connection.fetchall())


if __name__ == "__main__":
    app.run(debug=True)
