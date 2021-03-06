import os
from flask import Flask, request, redirect, session
from flask import render_template

from forms import RegisterForm, LoginForm
from model import db, Fcuser
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        pass

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    session.pop('userid', None)

    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # 회원 생성
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)
        db.session.commit()
        return redirect('/')

    return render_template("register.html", form=form)


@app.route('/')
def hello_world():
    userid = session.get('userid', None)

    return render_template("hello.html", userid=userid)


basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "1aagagagagagag"

csrf = CSRFProtect()
csrf.init_app(app)

db.init_app(app)
db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
