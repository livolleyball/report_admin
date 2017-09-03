# coding:utf8
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, equal_to, ValidationError
from app.models import User


class SendGoods_listdirect(FlaskForm):
    startdt=DateField('开始日期',[DataRequired()] ,format='%Y-%m-%d')
    endt = DateField('结束日期', [DataRequired()],format='%Y-%m-%d' )
    submit = SubmitField('查询')
