import os

from flask import Flask, session, request, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/reg")
def reg():
    return render_template('registration.html')

@app.route("/registration", methods  = ["POST","GET"])
def getRigistRequest():
    username = request.form.get("user")
    password = request.form.get("password")
    db.execute("insert into users (username, password) values (:username, :password);",{"username":username,"password":password})
    db.commit()
    return render_template('registration.html')

@app.route("/login", methods = ["POST","GET"])
def getLoginRequest():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")
        result = db.execute("select username from users where username=:username and password=:password",{"username":username,"password":password}).fetchall()
        if result == []:
            return render_template('fail.html')
        return render_template('success.html')
        db.commit()
    else:
        return render_template('login.html')

@app.route("/logout",methods = ["POST","GET"])
def logout():
    session.pop("username", None)
    return render_template('index.html')

@app.route("/search", methods=["POST", "GET"])
def search():
    return render_template("search.html")

@app.route("/search_result", methods=["POST", "GET"])
def search_result():
    keyword = "%" + request.form.get("keyword") + "%"
    
    
    # result = db.execute("SELECT * FROM books WHERE isbn LIKE :keyword or title LIKE :keyword or author LIKE :keyword or year LIKE :keyword;", {"keyword": keyword}).fetchall()

    result = db.execute(f"select * from books where isbn like '{keyword}' or title like '{keyword}' or author like '{keyword}' or year like '{keyword}'").fetchall()
    return render_template("search_result.html", result=result)


@app.route("/bookpage", methods=["POST", "GET"])
def bookpage():
    return render_template("bookpage.html", book=book)
