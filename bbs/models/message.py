from bbs import db

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

    def __init__(self, body, user_id, thread_id):
        self.body = body
        self.user_id = user_id
        self.thread_id = thread_id
