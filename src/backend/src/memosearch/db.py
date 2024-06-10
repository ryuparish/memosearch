import sqlite3
import click
from flask import current_app, g


def get_db(database_name='memos'):
    """Manage and get the global database connection (sqlite3)

    :returns: global flask database object for the respective database
    :rtype: sqlite3.Connection
    """

    if database_name in g:
        return g[database_name]
    else:
        g[database_name] = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g[database_name].row_factory = sqlite3.Row
        return g[database_name]


def close_db(database_name='memos', e=None):
    """Close connection if connection is still present
    We use e to catch errors that cause a teardown.

    :param e: Optional parameter because of close_db bug. Defaults to None
    :returns: None
    """
    db = g.pop(database_name, None)

    if db is not None:
        db.close()


def init_db(database_name='memos'):
    """
    Initialize database and load with schema sql file (schema.sql)

    :returns: None
    """
    db = get_db(database_name)

    with current_app.open_resource(database_name + '.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.

    :returns: None
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Setup teardown and add command to the application cli interface.

    :param app: The flask app to initialize.
    :type: Flask.app
    :returns: None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
