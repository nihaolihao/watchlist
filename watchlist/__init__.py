import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')  # 设置密钥

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix ='sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) # 实例化数据库对象
login_manager = LoginManager(app) # 实例化登录管理对象

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login' # 设置登录视图函数名称

# 模板上下文处理函数
@app.context_processor
def inject_user():  # 定义模板上下文处理函数
    from watchlist.models import User
    user = User.query.first()    # 取出第一个用户
    return dict(user=user)  # 返回字典

from watchlist import views, errors, commands