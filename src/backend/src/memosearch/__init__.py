import os
from flask import Flask
from .upload_blueprints import upload
from .retrieve_blueprints import retrieve
from flask_cors import CORS
from dotenv import load_dotenv

# Setting up environment variables
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'data.db'),
    )

    # loading the details for the application factory to attach
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register blueprints
    app.register_blueprint(upload)
    app.register_blueprint(retrieve)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    return app
