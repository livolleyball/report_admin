# coding:utf8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from config import config
from flask_admin import Admin
from app.Fadmin import CustomModelView, UserView,RoleView
from flask_login import LoginManager

# from app.models import Userlog,User
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
babel = Babel()
flask_admin = Admin()
from app.models import Userlog, User,Auth,Role,ParentAuth


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    flask_admin.init_app(app)

    # flask_admin.add_view(CustomView(name='Custom'))
    # Register view function `CustomModelView` into Flask-Admin
    flask_admin.add_view(UserView(User, db.session))
    flask_admin.add_view(RoleView(Role,db.session))
    models = [Userlog,Auth,ParentAuth]
    for model in models:
        flask_admin.add_view(
            CustomModelView(model, db.session, category='Models'))

    from app.home import home as home_blueprint
    # from app.datatable import datatable as datatable_blueprint
    from app.echarts import echarts as echarts_blueprint

    app.register_blueprint(home_blueprint)
    # app.register_blueprint(datatable_blueprint,url_prefix="/datatable")
    app.register_blueprint(echarts_blueprint, url_prefix="/echarts")

    return app
