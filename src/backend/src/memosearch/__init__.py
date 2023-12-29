import os
from flask import Flask
#from .extensions import db
from .upload_blueprints import upload
from .retrieve_blueprints import retrieve
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })

    # configure database options
    prefix = "sqlite:///"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", prefix + "data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # register blueprints
    app.register_blueprint(upload)
    app.register_blueprint(retrieve)

    # loading the details for the application factory to attach
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
