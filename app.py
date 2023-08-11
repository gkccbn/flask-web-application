import re
from flask import Flask, render_template,request, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_migrate import Migrate
import psycopg2
from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user
from datetime import datetime


#from userInfo import User
from config import *
app = Flask(__name__)
app.secret_key = 'mysecretkey'
POSTGRES_URL = CONFIG['postgresUrl']
POSTGRES_USER = CONFIG['postgresUser']
POSTGRES_PASS = CONFIG['postgresPass']
POSTGRES_DB = CONFIG['postgresDb']
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PASS, url=POSTGRES_URL, db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/projectDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)
#migrate = Migrate(app, db)
# def insert(): #insert
#
#     if request.method == 'POST':
#
#         uname = request.form['uname']
#         fname = request.form['fname']
#         mname = request.form['mname']
#         lname = request.form['lname']
#         bday = request.form['bday']
#         email = request.form['email']
#         passw = request.form['pass']
#
#         my_data = User(uname,fname,mname,lname,bday,email,passw)
#         db.session.add(my_data)
#         db.session.commit()
#
#         return redirect(url_for('register.html'))



@app.route('/')
def home():  # put application's code here
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname=request.form['uname']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        bday = request.form['bday']
        email = request.form['email']
        passw = request.form['passw']

        password=str(passw)
        if (len(password)<8):
            return "password must be at least 8  character long"
        if not re.search('[A-Z]', password):
            return "password must contain at least one capital letter"
        if not re.search('[a-z]', password):
            return "password must contain at least one lowercase letter"
        if not re.search('[0-9]', password):
            return"password must contain at least one digit"
        else:
            user = User.query.filter_by(userName=request.form.get("uname")).first()
            if user == request.form.get("uname"):
                return "kullanıcı bulunmakta"
            else:

                password = (sha256_crypt.encrypt(password))
                my_data = User(userName=uname, firstName=fname, middleName=mname, lastName=lname, birthDate=bday,email=email, password=password)
                db.session.add(my_data)
                ipAddress= request.remote_addr
                loginDateTime = datetime.now()
                db.session.commit()


                online_user = OnlineUsers(userName=uname, loginDateTime = loginDateTime, ipAddress=ipAddress)
                db.session.add(online_user)
                db.session.commit()
                return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():  # put application's code here
    if request.method == "POST":
        userName = request.form.get("uname")
        passw = request.form.get("passw")
        user = User.query.filter_by(userName=userName).first()
        admin=Admin.query.filter_by(username=userName).first()
        if admin is not None and admin.username==userName:
            return render_template('admin.html')
        elif user is None or not sha256_crypt.verify(passw,user.password):
            return "geri dön tülay"
        else:
            return redirect(url_for('page'))
    return render_template('login.html')
@app.route('/logout', methods = ['GET', 'POST'])
def logout():

    if request.method == 'POST':
        ipaddress = request.remote_addr
        onlineuser= OnlineUsers.query.filter_by(ipAddress=ipaddress).first()
        if onlineuser.ipAddress== ipaddress:
            loginDateTime = datetime.now()
            onlineuser.loginDateTime=loginDateTime
            db.session.add(onlineuser)
            db.session.commit()
            return render_template('home.html')
    return render_template('home.html')



@app.route('/user/create', methods = ['GET', 'POST'])
def create():

    return "created"

@app.route('/user/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        userid = request.form.get("id")
        user= User.query.filter_by(id=userid).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        else:
            return "user not found"
    return render_template('delete.html')

@app.route('/user/update',methods = ['GET', 'POST'])
def update():
    users=User.query.all()
    if request.method=='POST':
        id = request.form['id']
        uname=request.form['uname']
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        bday = request.form['bday']
        email = request.form['email']
        user =User.query.get(id)

        user.userName=uname
        user.firstName=fname
        user.middleName=mname
        user.lastName=lname
        user.birthDate=bday
        user.email=email

        db.session.commit()
    return render_template('update.html',users = users)

    # if request.method == 'POST':
    #     userid = request.form.get("id")
    #     user = User.query.filter_by(id=userid).first()
    #     if user is not None:
    #         return
    #
    #         db.session.commit()
    # return "update"
@app.route('/user/delete2',methods = ['GET', 'POST'])
def delete2():
    user = User.query.all()
    return render_template('delete2.html',users = user)

@app.route('/onlineusers')
def onlineusers():  # put application's code here
    return "onlineusers"

@app.route('/user/list', methods = ['GET', 'POST'])
def list():  # put application's code here
    onlineuser=OnlineUsers.query.all()

    return render_template('list.html',onlineuser = onlineuser)

@app.route('/admin')
def admin():  # put application's code here
    return render_template('admin.html')
@app.route('/page')
def page():  # put application's code here
    return render_template('page.html')



from userInfo import User
from onlineUser import OnlineUsers
from admin import Admin


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()