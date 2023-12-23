import os
import random
from flask import Flask
from flask import jsonify
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String
from flask_cors import cross_origin

# Setup
app = Flask(__name__)

prefix = "sqlite:///"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", prefix + "data.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Define Models and create tables
class Link(db.Model):
    __tablename__ = "links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    site_name: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)

    # This method is for printing.
    # It will show "<Student [firstname]>" as the type.
    def __repr__(self):
        return f"<Link id:{self.id}, site_name: {self.site_name}>"


class Screenshot(db.Model):
    __tablename__ = "screenshots"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    caption: Mapped[str] = mapped_column(String)
    text_in_image: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Screenshot id:{self.id}, caption: {self.caption}>"


class Note(db.Model):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    about: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    related_activity: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f"<Screenshot id:{self.id}, about: {self.about}>"


# Create all the Models into tables above
with app.app_context():
    db.create_all()


# Routes
@app.route("/search", methods=["POST", "OPTIONS"])
@cross_origin()
def search():
    """Handles the search route.

    POST: This route returns all the matching results from the query.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    # Process request (return list of dicts)
    if request.method == "POST":
        curr_results = {k: [] for k in request_data["content"]}

        # Adding site-name-matched links to the result list
        if ("links" in request_data["content"]):
            results = Link.query.filter_by(
                site_name=request_data["search"]
            ).all()

            for result in results:
                curr_results["links"] += [{
                    "id": result.id,
                    "about": result.about,
                    "link": result.link,
                    "site_name": result.site_name,
                    "related_activity": result.related_activity
                }]
                print(result.link)

        # Adding caption-matched screenshots to the result list
        if ("screenshots" in request_data["content"]):
            results = Screenshot.query.filter_by(
                caption=request_data["search"]
            ).all()

            for result in results:
                curr_results["screenshots"] += [{
                    "id": result.id,
                    "about": result.about,
                    "date": result.date,
                    "caption": result.caption,
                    "text_in_image": result.test_in_image,
                    "related_activity": result.related_activity
                }]

        # Adding title-matched notes to the result list
        if ("notes" in request_data["content"]):
            results = Note.query.filter_by(
                title=request_data["search"]
            ).all()

            for result in results:
                curr_results["notes"] += [{
                    "id": result.id,
                    "about": result.about,
                    "date": result.date,
                    "related_activity": result.related_activity
                }]

        response = jsonify(curr_results)
        print(curr_results)
        return response


@app.route("/links", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def links():
    """Handles the link route.

    GET: This route gets information about the link
    and returns it in a dictionary.

    POST: This route adds information about the link
    and returns the result in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    if request.method == "POST":
        # Link validation for POST
        # Try to use urlopen
        try:
            html = urlopen(request_data["link"]).read()
        except Exception as e:
            print(f"Error opening URL: {e}")
            return f"Error opening URL: {e}"

        # Check for empty link
        if len(request_data["link"]) == 0:
            print(f"Error, link is empty: {request_data['link']}")
            return f"Error, link is empty: {request_data['link']}"

        # Process the text
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # Get text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        # Data for database.
        id = random.getrandbits(16)
        link = request_data["link"]
        about = request_data["linkAbout"]
        date = request_data["linkDate"]
        site_name = urlparse(request_data["link"]).netloc
        related_activity = request_data["linkActivity"]

        # Getting data from request and adding to the database.
        new_link = Link(
            id=id,
            link=link,
            about=about,
            date=date,
            site_name=site_name,
            related_activity=related_activity,
        )

        new_dict_link = {
            "id": id,
            "link": link,
            "about": about,
            "date": date,
            "site_name": site_name,
            "related_activity": related_activity,
        }

        # Prevent duplicates
        if len(Link.query.filter_by(link=link).all()) == 0:
            print("Query Link is not yet known, adding to database")
            db.session.add(new_link)
            db.session.commit()

        response = jsonify([new_dict_link])
        return response
