from flask_wtf import FlaskForm
from flask_admin.form import Select2TagsField, Select2Field
from flask_admin.form.widgets import Select2TagsWidget
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, RadioField
from wtforms.validators import DataRequired, Length, Email, equal_to, ValidationError, url
from wtforms.fields.html5 import URLField, DateField, DateTimeLocalField, EmailField, DecimalField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets.html5 import DateInput, DateTimeInput
from wtforms.widgets import PasswordInput, CheckboxInput, Select, SubmitInput, TextInput
from app.models import User


# class SubmitField(BooleanField):
#     """
#     Represents an ``<input type="submit">``.  This allows checking if a given
#     submit button has been pressed.
#     """
#     widget = SubmitInput()
class MyTextInput(TextInput):
    def __init__(self, error_class=u'has_errors'):
        super(MyTextInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        return super(MyTextInput, self).__call__(field, **kwargs)


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


class Quickwtf(FlaskForm):
    url = URLField(validators=[url()])
    SelectMultipleField = SelectMultipleField('MS', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text'),
                                                             ('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text'),
                                                             ('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    dt = DateField('date')
    dt1 = DateTimeField('datetime', widget=DateInput())
    RadioField = RadioField('RadioField', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    password = PasswordField('新密码')
    submit = SubmitField('更新密码')
    mytext = MyTextInput('mytext1')
    select2 = Select2Field('select2', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    select2T = Select2TagsField('select22', coerce=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')],
                                widget=Select2TagsWidget())
