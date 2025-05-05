import click
from watchlist import app, db
from watchlist.models import User, Movie

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
