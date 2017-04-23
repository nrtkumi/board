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
