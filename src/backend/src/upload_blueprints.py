import os
import random
import json
from flask import jsonify
from urllib.parse import urlparse
from flask import Blueprint, request
from flask_cors import cross_origin
from .extensions import db
from .models import Note, Screenshot, Link


upload = Blueprint('upload', __name__, template_folder='templates')
# Routes
@upload.route("/screenshots", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def screenshots():
    """Handles the note route.

    GET: This route gets information about the note
    and returns it in a dictionary.

    POST: This route adds information about the note
    and returns the result in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_form = request.form

    if request.method == "POST":
        # Check for empty screenshot
        if request.files["file"] is None or request.files["file"].filename == "":
            print("file is empty returning nothing")
            return "Error, file is empty"

        # Upload file to our directory
        id = random.getrandbits(16)
        target = os.environ.get("UPLOAD_FOLDER")
        if not os.path.isdir(target):
            os.mkdir(target)

        file = request.files['file']
        filename = str(id)
        destination = "/".join([target, filename])
        file.save(destination)

        # Data for database.
        # The file is replaced with the path to the file in the
        # UPLOAD_FOLDER because we dont need to save an entire image in
        # the database.
        about = request_form["about"]
        date = request_form["date"]
        caption = request_form["caption"]
        text_in_image = request_form["text"]
        path = destination
        related_activity = request_form["activity"]
        view = request_form["view"]

        # # Getting data from request and adding to the database.
        new_screenshot = Screenshot(
            id=id,
            about=about,
            caption=caption,
            date=date,
            text_in_image=text_in_image,
            path=path,
            related_activity=related_activity,
            view=view,
        )

        new_dict_screenshot = {
            "id": id,
            "about": about,
            "caption": caption,
            "date": date,
            "text_in_image": text_in_image,
            "path": path,
            "related_activity": related_activity,
            "view": view
        }

        # Do not prevent duplicates
        db.session.add(new_screenshot)
        db.session.commit()

        response = jsonify([new_dict_screenshot])
        return response

@upload.route("/views", methods=["GET", "OPTIONS"])
@cross_origin()
def views():
    """Handles the link route.

    GET: This route gets information about the link
    and returns it in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    if request.method == "GET":
        all_views = set(["all"])
        for table in [Note, Link, Screenshot]:
            for value in table.query.distinct(table.view).group_by(table.view):
                print(value)
                all_views.add(value)
        return list(all_views)

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
    for json_data in request_data:
        print('Here is one of the json: ' + json.dumps(json_data))

    if request.method == "POST":
        # Link validation for POST
        # Check for empty link
        if len(request_data) == 0:
            print(f"Error, link is empty: {request_data}")
            return f"Error, link is empty: {request_data}"


        new_links = []
        for json_data in request_data:
            # Data for database.
            id = random.getrandbits(16)
            link = json_data["link"]
            about = json_data["about"]
            date = json_data["date"]
            site_name = json_data["site_name"]
            related_activity = json_data["related_activity"]
            view = json_data["view"]

            # Getting data from json and adding to the database.
            new_link = Link(
                id=id,
                link=link,
                about=about,
                date=date,
                site_name=site_name,
                related_activity=related_activity,
                view=view,
            )

            new_dict_link = {
                "id": id,
                "link": link,
                "about": about,
                "date": date,
                "site_name": site_name,
                "related_activity": related_activity,
                "view": view,
            }

            # Prevent duplicates
            if len(Link.query.filter_by(link=link).all()) == 0:
                print("Query Link is not yet known, adding to database")
                db.session.add(new_link)
                db.session.commit()
                new_links.append(new_dict_link)

        response = jsonify(new_links)
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
        view = request_data["view"]

        # Getting data from request and adding to the database.
        new_note = Note(
            id=id,
            title=noteTitle,
            about=about,
            date=date,
            related_activity=related_activity,
            view=view,
        )

        new_dict_note = {
            "id": id,
            "title": noteTitle,
            "about": about,
            "date": date,
            "related_activity": related_activity,
            "view": view,
        }

        # Prevent duplicates
        if len(Note.query.filter_by(title=noteTitle).all()) == 0:
            print("Query Note is not yet known, adding to database and writing file")
            db.session.add(new_note)
            db.session.commit()

        response = jsonify([new_dict_note])
        return response
