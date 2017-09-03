from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, equal_to, ValidationError
from app.models import User


class LoginFrom(FlaskForm):
    # email = StringField('邮箱', validators=[DataRequired(), Length(1, 20), Email()],
    #                     render_kw={"class": "input-text size-L ", "placeholder": "请输入邮箱"})
    # password = PasswordField('密码', validators=[DataRequired()],
    #                          render_kw={"class": "input-text size-L ", "placeholder": "请输入密码"})
    # remember_me = BooleanField('记住密码')
    # submit = SubmitField('登陆', render_kw={"class": "btn btn-success radius size-L"})
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原始密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), equal_to('password2', message='Passwords must match')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('更新密码')
