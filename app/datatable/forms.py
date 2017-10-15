# coding:utf8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, SelectMultipleField, RadioField, DateTimeField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import DateInput
from wtforms_components import SelectMultipleField as optSelectMultipleField


class SendGoods_listdirect(FlaskForm):
    startdt = DateField('开始日期', [DataRequired()], format='%Y-%m-%d')
    endt = DateField('结束日期', [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('查询')


class Buiform(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired('请输入用户名')],
                           description='用户名',
                           render_kw={'class': 'control-text', 'placeholder': '输入用户名', 'required': "required"})
    optSelectMultipleField = optSelectMultipleField('optMS', choices=(
        ('Fruits', (
            ('apple', 'Apple'),
            ('peach', 'Peach'),
            ('pear', 'Pear')
        )),
        ('Vegetables', (
            ('cucumber', 'Cucumber'),
            ('potato', 'Potato'),
            ('tomato', 'Tomato'),
        ))
    ),
                                                    default=('cpp', 'C++'))
    SelectMultipleField = SelectMultipleField('MS', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text'),
                                                             ('cpp1', 'C1++'), ('py1', 'Python1'),
                                                             ('text1', 'Plain Text1')],
                                              default=('cpp', 'C++'))
    dt = DateField('日期')
    dt1 = DateTimeField('datetime', widget=DateInput())
    RadioField = RadioField('RadioField', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    city1 = SelectField('省', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    select = SelectField('单选', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    password = PasswordField('新密码')
    submit = SubmitField('提交查询')
    # mytext = MyTextInput('mytext1')


class CityByCityIdForm(FlaskForm):
    starttime = DateField('开始日期')
    endtime = DateField('结束日期')
    mobile1 = StringField('创建人手机号码')
    mobile2 = StringField('服务站手机号码')
    classify = SelectField('主营业务', choices=[('全选', '全选'), ('餐饮店', '餐饮店'), ('住宿宾馆', '住宿宾馆')], default=('全选', '全选'))
    province = SelectField('省', choices=[('0', '全选')], render_kw={"onchange": "getCity(this.value)"})
    city = SelectField('市', choices=[('0', '全选')])
    authstarttime = DateField('审核开始日期')
    authendtime = DateField('审核结束日期')
    submit = SubmitField('查询')
