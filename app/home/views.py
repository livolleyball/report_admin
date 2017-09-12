# coding:utf8
from flask_login import login_user, logout_user, login_required, current_user
from . import home
from .. import db
from ..models import User
from flask import render_template, redirect, url_for, flash
from .forms import LoginFrom, ChangePasswordForm,Quickwtf
from werkzeug.security import generate_password_hash


@home.route("/")
@login_required
def index():
    return render_template("index.html")


@home.route("/login", methods=["GET", "POST"])
def login():
    '''登陆'''
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('home.index'))
        flash('用户不存在或者密码错误！', 'err')
    return render_template('home/login.html', form=form)


@home.route("/logout/")
@login_required
def logout():
    logout_user()
    flash('您已经退出')
    return redirect(url_for("home.login"))

@home.route("/quickwtf/")
def quickwtf():
    form=Quickwtf()
    return render_template('home/quickwtf.html',form=form)


@home.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = generate_password_hash(form.password.data)
            db.session.add(current_user)
            flash('密码已更新')
            # return redirect(url_for('main.index'))
        else:
            flash('密码错误.')
    return render_template("home/change_password.html", form=form)
