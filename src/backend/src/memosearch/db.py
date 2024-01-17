import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Get the global database connection (sqlite3)
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Close connection if connection is still present
    We use e to catch errors that cause a teardown.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize database and load with schema sql file
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Setup teardown and add command to the application cli interface.

    :param app Flask.app: The flask app to initialize
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
