import click
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

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
login_manager = LoginManager(app)

login_manager.login_view = 'login'
@app.route('/',methods=['GET','POST'])
def index():
    # return 'Welcome to My Watchlist!'
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
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

@login_required
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

@login_required
@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.')
    return redirect(url_for('index'))

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

# 创建数据库模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

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

@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')