from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
    nickname = StringField('nickname:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])

class ArticleForm(Form):
    title = StringField('title:', validators=[DataRequired()])
    text = TextAreaField('text:', validators=[DataRequired()])
