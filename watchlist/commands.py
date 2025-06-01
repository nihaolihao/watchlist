import click
from watchlist import db, app
from watchlist.models import User, Movie

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