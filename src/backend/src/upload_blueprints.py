import os
from flask import Flask
import random
from flask import jsonify
from urllib.parse import urlparse
from flask import Blueprint, abort, request, render_template
from flask_cors import cross_origin
from thefuzz import fuzz
from .extensions import db
from .models import Note, Screenshot, Link

upload = Blueprint('upload', __name__, template_folder='templates')
# Routes



@upload.route("/links", methods=["GET", "POST", "OPTIONS"])
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
        # Check for empty link
        if len(request_data["link"]) == 0:
            print(f"Error, link is empty: {request_data['link']}")
            return f"Error, link is empty: {request_data['link']}"

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


@upload.route("/notes", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def notes():
    """Handles the note route.

    GET: This route gets information about the note
    and returns it in a dictionary.

    POST: This route adds information about the note
    and returns the result in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    if request.method == "POST":
        # Check for empty note
        if len(request_data["noteTitle"]) == 0:
            print(f"Error, note title is empty: {request_data['noteTitle']}")
            return f"Error, note title is empty: {request_data['noteTitle']}"

        # Data for database.
        id = random.getrandbits(16)
        noteTitle = request_data["noteTitle"]
        about = request_data["noteAbout"]
        date = request_data["noteDate"]
        related_activity = request_data["noteActivity"]

        # Getting data from request and adding to the database.
        new_note = Note(
            id=id,
            title=noteTitle,
            about=about,
            date=date,
            related_activity=related_activity,
        )

        new_dict_note = {
            "id": id,
            "title": noteTitle,
            "about": about,
            "date": date,
            "related_activity": related_activity,
        }

        # Prevent duplicates
        if len(Note.query.filter_by(title=noteTitle).all()) == 0:
            print("Query Note is not yet known, adding to database and writing file")
            db.session.add(new_note)
            db.session.commit()

        response = jsonify([new_dict_note])
        return response
