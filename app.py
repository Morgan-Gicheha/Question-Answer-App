from flask import Flask,render_template,request,redirect,url_for, flash,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import LoginManager,logout_user,login_fresh,login_required,logout_user, login_user, current_user
import random
import psycopg2

app= Flask(__name__)

# db = SQLAlchemy(app)

# SYSTEM CONFIGURATIONS
# postgresql://scott:tiger@localhost/mydatabase
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:morgan8514@127.0.0.1:5432/QA_app"
app.config["SECRET_KEY"]="secretrer"

db = SQLAlchemy(app)
# connecting to an existing database in order to use psycopg2
conn = psycopg2.connect("dbname=QA_app user=postgres password=morgan8514")
cur = conn.cursor()

# configuring flask-login
login_manager =  LoginManager(app)
login_manager.login_view= "login"
login_manager.login_message="please login to view this page"

# creating user_loader
@login_manager.user_loader
def user_loader(user_id):
    user_obj = User_qa.query.filter_by(id= user_id).first()
    return user_obj

# importing models
from models.users_qa import User_qa
from models.questions import Questions_qa

@app.before_first_request
def create():
    db.create_all()





# importing WTForms
from form_wtf.registeration import Register_qa
from form_wtf.login import Login


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
             
            flash("Account created! Login ..","error")
            return redirect(url_for("login"))
           



    return render_template("register.html",form=form)

@app.route("/login",methods=["POST","GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        if request.method=="POST":
            name = form.name.data
            password = form.password.data
            # searching for username
            search_username= User_qa.query.filter_by(name=name).first()
            if search_username:
                password_check = User_qa.search_name_and_password(search_username.name,password)
                if password_check:
                    login_user(search_username,remember=False)
                    flash("loggin succes")
                    return redirect(url_for("home"))

                else:
                    message= "login not succesfull password_check "
                    flash(message,'warning')
                    return redirect(url_for("login"))
                
            else:
                message= "login not succesfull username"
                flash(message)
                return redirect(url_for("login"))
                



    return render_template("login.html",form=form)


@app.route("/")
@login_required
def home():
    return render_template("home.html")

@app.route("/ask",methods=["POST","GET"])
@login_required
def ask():

    # quering for experts
    experts =cur.execute("SELECT * FROM user_qa WHERE IS_EXPERT=True;")
    experts=cur.fetchall()
    if request.method=="POST":
        question = request.form["question"]
        expert_id= request.form["expert_id"]

        # committing to db
        question_to_db= Questions_qa(question=question,expert_id=expert_id)
        question_to_db.create()

    return render_template("ask.html",experts=experts)

@app.route("/answer")
@login_required
def answer():
    return render_template("answer.html")

# route views unanswered question for the expert
@app.route("/unanswered")
@login_required
def unanswered():
    logged_user= current_user.id
    questions_per_expert=cur.execute("SELECT * FROM questions_qa WHERE expert_id={};".format(logged_user))

    questions_per_expert=cur.fetchall()

    

    
    
    return render_template("unanswered.html")

@app.route("/users",methods=["POST","GET"])
@login_required
def users():
    # quering all users
    users= User_qa.query.all()

    return render_template("users.html", users=users)

# rout to promot users to experts
@app.route("/promote/<username>",methods=["GET"])
def promote(username):

    if request.method == "GET":
        print(username)
        User_qa.promote(username)

    return redirect(url_for("users"))

# this route fetche sthe alst question aske and should be viewd by  user
@app.route("/question")
@login_required
def question():
    return render_template ("question.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))



if __name__=="__main__":
    app.run(debug=True)