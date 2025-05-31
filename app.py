import click
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys
app = Flask(__name__)
app.debug = True  # 开启调试模式
app.config['SECRET_KEY'] = 'dev'
WIN = sys.platform.startswith('win')
if WIN:
    prefix ='sqlite:///'
else:
    prefix ='sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)
@app.route('/',methods=['GET','POST'])
def index():
    # return 'Welcome to My Watchlist!'
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))


    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit',movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

# 创建数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 自定义命令initdb
@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 定义虚拟数据

    name = 'Li Hao'
    movies = [
        {'title': 'The Shawshank Redemption', 'year': 1994},
        {'title': 'The Godfather', 'year': 1972},
        {'title': 'The Dark Knight', 'year': 2008},
        {'title': '12 Angry Men', 'year': 1957},
        {'title': 'Schindler\'s List', 'year': 1993},
        {'title': 'The Lord of the Rings: The Return of the King', 'year': 2003},
        {'title': 'Pulp Fiction', 'year': 1994},
        {'title': 'The Lord of the Rings: The Fellowship of the Ring', 'year': 2001},
        {'title': 'The Good, the Bad and the Ugly', 'year': 1966},
        {'title': 'Fight Club', 'year': 1999}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')