# coding:utf8

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


# 会员
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 姓名
    email = db.Column(db.String(100))  # 邮箱
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    password = db.Column(db.String(100))  # 密码
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间

    # user_id = db.relationship('Userlog', backref='user')

    # pythonic使用@property将方法变成属性
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def __repr__(self):
        return self.name

    # def is_admin(self):
    #     return self.role_id == Role.query.fillter_by(name='admin').first()
        # return is_admin(self.role_id,value)


# Create M2M table
role_auth_table = db.Table('role_auth', db.Model.metadata,
                           db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                           db.Column('auth_id', db.Integer, db.ForeignKey('auth.id'))
                           )


# 角色
class Role(db.Model):  # 角色
    __tablename__ = "role"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    nickname = db.Column(db.String(100), unique=True)  # 中文名称
    # auths = db.Column(db.String(600))  # 角色权限列表
    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    users = db.relationship("User", backref='role')  # 在关系的另一个模型中添加反向引用
    auths = db.relationship("Auth", secondary=role_auth_table)

    def __int__(self, name, nickname, auths):
        self.name = name
        self.nickname = nickname
        self.auths = auths

    def __repr__(self):
        return self.name + '-' + self.nickname



# 菜单树结构
class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(100))
    description = db.Column(db.Text())
    authlevel=db.Column(db.Integer)
    # parent_id = db.Column(db.Integer, db.ForeignKey('parent_auth.id'))  # 所属角色
    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间
    parent_id = db.Column(db.Integer, db.ForeignKey('auth.id'))
    parent = db.relationship('Auth', remote_side=[id], backref='children')

    def __str__(self):
        return self.name


# class ParentAuth(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     url = db.Column(db.String(100))
#     description = db.Column(db.Text())
#     addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间
#     children = db.relationship("Auth", backref='parent')  # 用户外键关系关联
#
#     # parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
#     # parent = db.relationship('Auth', remote_side=[id], backref='children')
#
#     def __str__(self):
#         return self.name

# 会员登陆日志
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # 外键约束并不好用
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Userlog %r>' % self.id


class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    parent_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
    parent = db.relationship('Tree', remote_side=[id], backref='children')

    def __str__(self):
        return self.name


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
