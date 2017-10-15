# coding:utf8
from flask import redirect, url_for, flash, request
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from wtforms.validators import DataRequired, Email

from app.models import Auth


# from app.models import User

class MyHomeView(AdminIndexView):
    def is_accessible(self):
        # if current_user.is_anonymous:
        #     return redirect(url_for('home.login'))
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash('admin 后台只对管理员开放')
        return redirect(url_for('home.login', next=request.url))

    @expose('/')
    @login_required
    def index(self):
        print(type(current_user.role.name))
        print(type(current_user.name))

        print(current_user.role.name)
        print(current_user.role.name=='admin')
        return self.render("admin/baseadmin.html")


class AccessView(ModelView):
    """View function of Flask-Admin for Models page."""
    def is_accessible(self):
        # if current_user.is_anonymous:
        #     return redirect(url_for('home.login'))
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash('admin 后台只对管理员开放')
        return redirect(url_for('home.login'))


class UserView(AccessView):
    column_descriptions = dict(
        name='First and Last name'
    )
    column_labels = dict(
        name=u'用户名',
        email=u'邮箱',
        password=u'密码',
        addtime=u'注册时间',
        role=u'角色'

    )
    form_args = dict(
        email=dict(validators=[Email()], render_kw={"placeholder": "请输入邮箱"}),
        # email=dict(validators=[Email()], render_kw={"placeholder": "请输入邮箱", "readonly": "readonly"}),
        password=dict(validators=[DataRequired()]),
    )
    column_exclude_list = (

        'password',

    )

    page_size = 15

    # form_extra_fields = {
    #     'password': PasswordField('密码', validators=[DataRequired()])
    # }

    def on_model_change(self, form, User, is_created=False):
        # 调用用户模型中定义的set方法
        User.set_password(form.password.data)



class RoleView(AccessView):
    # form_excluded_columns = ['users', ]
    column_labels = dict(
        name=u'角色名',
        nickname=u'昵称',
        addtime=u'注册时间',
        users=u'用户',
        auths=u'菜单'
    )


class AuthAdmin(AccessView):
    column_labels = dict(
        name=u'菜单名',
        url=u'链接',
        parent=u'父菜单',
        description=u'需求描述',
        addtime=u'注册时间',
        users=u'用户',
        auths=u'菜单',
        children=u'子菜单'
    )

    form_args = dict(
        # url=dict(label='链接', validators=[DataRequired(), url()]),
        url=dict(label='链接', validators=[DataRequired()]),
        parent=dict(label='父菜单')
    )
    can_set_page_size = True

    def create_form(self):
        return self._use_filtered_parent(
            super(AuthAdmin, self).create_form()
        )

    def edit_form(self, obj):
        return self._use_filtered_parent(
            super(AuthAdmin, self).edit_form(obj)
        )

    def _use_filtered_parent(self, form):
        form.parent.query_factory = self._get_parent_list
        return form

    def _get_parent_list(self):
        # only show available pets in the form
        return Auth.query.filter(Auth.authlevel < 3).all()
        # return Auth.query.all()