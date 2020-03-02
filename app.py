from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash ,check_password_hash
import random

app= Flask(__name__)

# db = SQLAlchemy(app)

# SYSTEM CONFIGURATIONS
# postgresql://scott:tiger@localhost/mydatabase
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:morgan8514@127.0.0.1:5432/QA_app"
app.config["SECRET_KEY"]="secretrer"

db = SQLAlchemy(app)

# importing models
from models.users_qa import User_qa

@app.before_first_request
def create():
    db.create_all()





# importing WTForms
from form_wtf.registeration import Register_qa


@app.route("/register",methods=["POST","GET"])
def register():
    form = Register_qa()
    if form.validate_on_submit():
        if request.method=='POST':
            name = form.name.data
            email =  form.email.data
            password = form.password.data

            hashed_password = generate_password_hash(password)
            data = User_qa(email=email,name=name,password=hashed_password)
            data.create()
            message= "Account created!"
            return render_template("login.html",form=form, message=message)
           



    return render_template("register.html",form=form)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/ask")
def ask():
    return render_template("ask.html")

@app.route("/answer")
def answer():
    return render_template("answer.html")

@app.route("/unanswered")
def unanswered():
    return render_template("unanswered.html")

@app.route("/users")
def users():
    return render_template("users.html")

@app.route("/question")
def question():
    return render_template ("question.html")



if __name__=="__main__":
    app.run(debug=True)