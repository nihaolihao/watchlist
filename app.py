# -*- coding: utf-8 -*-
import os
import sys
import click
from flask import Flask, url_for,render_template
from flask_sqlalchemy import SQLAlchemy



WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix ='sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) # 实例化数据库对象

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




@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    # return 'Welcome to My Watchlist!'
    user = User.query.first()    # 取出第一个用户
    movies = Movie.query.all()   # 取出所有电影
    return render_template('index.html',name=name,movies=movies)

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

class User(db.Model): # 定义User模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(50)) # 姓名

class Movie(db.Model): # 定义Movie模型
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影名
    year = db.Column(db.String(4)) # 年份



if __name__ == '__main__':
    app.run(debug=True)