from bbs import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))
    threads = db.relationship('Thread', backref = 'user')
    messages = db.relationship('Message', backref = 'user')

    def __init__(self, name, email, password, token):
        self.name = name
        self.email = email
        self.password = password
        self.token = token
