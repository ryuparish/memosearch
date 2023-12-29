import os
from flask import Flask
from .extensions import db
from .upload_blueprints import upload
from .retrieve_blueprints import retrieve
from flask_cors import CORS

# Setup
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

# Setup database with sqlite connection
# This changes if the application is a module vs. a package.
prefix = "sqlite:///"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", prefix + "data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(upload)
app.register_blueprint(retrieve)

# Create all the Models into tables above
with app.app_context():
    db.init_app(app)
    db.create_all()
