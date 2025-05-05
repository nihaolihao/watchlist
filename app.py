# -*- coding: utf-8 -*-
import os
import sys
import click
from flask import Flask, url_for,render_template,redirect,flash,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix ='sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) # 实例化数据库对象

login_manager = LoginManager(app) # 实例化登录管理对象
login_manager.login_view = 'login' # 设置登录视图函数名
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('login'))  # 重定向回登录页面
        
        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户
            flash('Login success.')  # 显示成功信息
            return redirect(url_for('index'))  # 重定向回首页
        
        flash('Invalid username or password.')  # 显示错误信息
        return redirect(url_for('login'))  # 重定向回登录页面
    
    return render_template('login.html')  # 登录页面

@app.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Logout success.')  # 显示成功信息
    return redirect(url_for('index'))  # 重定向回登录页面

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.cli.command() # 定义命令行命令
@click.option('--drop', is_flag=True, help='Create after drop.') # 定义选项
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'lihaonihao'
    movies = [
        {
            'title': 'My Neighbor Totoro','year':'1988'
        },
        {
            'title': 'Three Colours trilogy','year':'1993'
        },
        {
            'title': 'Forrest Gump','year':'1994'
        },
        {
            'title': 'Memento','year':'2000'
        }
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


app.config['SECRET_KEY'] = 'dev'  # 设置密钥

@app.route('/',methods=['GET','POST'])
@app.route('/index')
@app.route('/home')
def index():
    # return 'Welcome to My Watchlist!'
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))  # 未登录则重定向到登录页面
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('index'))  # 重定向回首页
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页
    
    user = User.query.first()    # 取出第一个用户
    movies = Movie.query.all()   # 取出所有电影
    return render_template('index.html',movies=movies)

@app.route('/delete/<int:movie_id>',methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 根据电影ID取出电影，如果不存在则返回404错误
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')  # 显示成功信息
    return redirect(url_for('index'))  # 重定向回首页
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'

@app.errorhandler(404)  # 定义404错误处理函数
def page_not_found(e):
    user = User.query.first()    # 取出第一个用户
    return render_template('404.html'), 404  # 返回404页面

# 模板上下文处理函数
@app.context_processor
def inject_user():  # 定义模板上下文处理函数
    user = User.query.first()    # 取出第一个用户
    return dict(user=user)  # 返回字典

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 根据电影ID取出电影，如果不存在则返回404错误
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(title) > 60 or len(year) > 4:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回编辑页面
        
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页
    return render_template('edit.html', movie=movie)  # 编辑电影信息页面
# 定义虚拟数据
name = 'lihaonihao'
movies = [
    {
        'title': 'My Neighbor Totoro','year':'1988'
    },
    {
        'title': 'Three Colours trilogy','year':'1993'
    },
    {
        'title': 'Forrest Gump','year':'1994'
    },
    {
        'title': 'Memento','year':'2000'
    }
]

class User(db.Model, UserMixin): # 定义User模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(50)) # 姓名
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Model): # 定义Movie模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影名
    year = db.Column(db.String(4)) # 年份


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user with admin privileges."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')  # 显示错误信息
            return redirect(url_for('settings'))  # 重定向回设置页面
        
        current_user.name = name
        db.session.commit()
        flash('Settings updated.')  # 显示成功信息
        return redirect(url_for('index'))  # 重定向回首页

    return render_template('settings.html')  # 设置页面

if __name__ == '__main__':
    app.run(debug=True)