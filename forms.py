from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, EqualTo

from model import Fcuser


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired(), EqualTo('repassword')])
    repassword = StringField('repassword', validators=[DataRequired()])


class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data

            fcuser = Fcuser.query.filter_by(userid=userid).first()

            if fcuser.password != password:
                raise ValueError('Wrong password')


    userid = StringField('userid', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired(), UserPassword()])
