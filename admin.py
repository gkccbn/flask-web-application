from app import db
#db.init_app(app)
class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))



    def __init__(self, userName, password):
        self.userName = userName
        self.password = password



