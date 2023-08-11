from app import db
from flask_login import UserMixin
#db.init_app(app)
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique = True)
    firstName = db.Column(db.String(20))
    middleName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    birthDate = db.Column(db.Date())
    email = db.Column(db.String(20))
    password = db.Column(db.String(80))

    def __init__(self, userName, firstName, middleName, lastName, birthDate, email, password):
        self.userName = userName
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.birthDate = birthDate
        self.email = email
        self.password = password




#with app.app_context():
#    db.create_all()





