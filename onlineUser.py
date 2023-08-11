from app import db
from flask_login import UserMixin
#db.init_app(app)
class OnlineUsers(UserMixin,db.Model):
    __tablename__ = 'onlineuser'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(20), unique = True)
    ipAddress = db.Column(db.String(20))
    loginDateTime = db.Column(db.Date())


    def __init__(self, userName, ipAddress, loginDateTime):
        self.userName = userName
        self.ipAddress = ipAddress
        self.loginDateTime = loginDateTime

