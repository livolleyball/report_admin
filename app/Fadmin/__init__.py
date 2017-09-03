# coding:utf8
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
# from app.models import User


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    pass


class UserView(ModelView):
    page_size = 15

    def on_model_change(self, form, User, is_created=False):
        # 调用用户模型中定义的set方法
        User.set_password(form.password.data)

class RoleView(ModelView):
    form_excluded_columns = ['users', ]