from bbs import db

class Thread(db.Model):
    __tablename__ = 'thread'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship('Message', backref = 'thread')

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
