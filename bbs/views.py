from flask import request, redirect, url_for, render_template, flash, make_response
from bbs import app, db
from bbs.models.user import User
from bbs.models.thread import Thread
from bbs.models.message import Message
import uuid

@app.before_request
def before_request():
    if request.cookies.get('bbs_uid') is not None:
        return
    elif request.path == '/login':
        return
    elif request.path == '/signup':
        return
    else:
        return redirect(url_for('login'))

@app.route('/')
def root():
    #print("XXXXXXXXXXXXXXXXXXXXXXX")
    #a = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
    #print(a)
    #print("XXXXXXXXXXXXXXXXXXXXXXXX")
    data = {}
    data["user"] = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
    return render_template('root.html', data = data)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] and request.form['password']:
            user = User.query.filter_by(email = request.form['email']).first()
            if user is None or user.password != request.form['password']:
                flash('emailかパスワードが間違っています')
                return render_template('login.html')
            res = make_response(redirect(url_for('root')))
            res.set_cookie('bbs_uid', user.token)
            flash('ログイン成功')
            return res
        else:
            flash('入力に不備があります')
    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if request.form['name'] and request.form['email'] and request.form['password']:
            uid = uuid.uuid4().hex
            user = User(name = request.form['name'],
                        email = request.form['email'],
                        password = request.form['password'],
                        token = uid)
            db.session.add(user)
            db.session.commit()

            data = {}
            data["user"] = User.query.filter_by(token = uid).first()

            #res = make_response(render_template('root.html', data = data))
            res = make_response(redirect(url_for('root')))
            res.set_cookie('bbs_uid', uid)

            flash('ユーザー作成成功')
            return res
        else:
            flash('入力に不備があります')
    return render_template('signup.html')

@app.route('/thread/new')
def new_thread():
    return render_template('new_thread.html')

@app.route('/thread', methods = ['POST'])
def create_thread():
    if request.form['title']:
        user = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
        thread = Thread(title = request.form['title'],
                        user_id = user.id)
        db.session.add(thread)
        db.session.commit()
        return redirect(url_for('all_thread'))

@app.route('/threads')
def all_thread():
    threads = Thread.query.order_by(Thread.id.desc()).all()
    return render_template('all_thread.html', threads = threads)

@app.route('/threads/<thread_id>')
def show_thread(thread_id):
    data = {}
    data['thread_id'] = thread_id
    data['user'] = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
    data['messages'] = Message.query.filter_by(thread_id = thread_id).all()
    return render_template('show_thread.html', data = data)

@app.route('/threads/<thread_id>/send', methods = ['POST'])
def send_message(thread_id):
    if request.form['body']:
        user = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
        message = Message(body = request.form['body'],
                          user_id = user.id,
                          thread_id = thread_id)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('show_thread', thread_id = thread_id))

@app.route('/edit_mesage/<message_id>')
def edit_message(message_id):
    user = User.query.filter_by(token = request.cookies.get('bbs_uid')).first()
    message = Message.query.get(message_id)
    if user.id != message.user_id:
        return redirect(url_for('root'))
    return render_template('edit_message.html', message = message)

@app.route('/edit/<message_id>', methods = ['POST'])
def update_message(message_id):
    new_body = request.form['body']
    message = Message.query.filter_by(id = message_id).first()
    message.body = new_body
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('show_thread', thread_id = message.thread_id))
