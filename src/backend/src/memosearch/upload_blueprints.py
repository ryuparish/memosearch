import os
import random
import json
from flask import jsonify, current_app
from urllib.parse import urlparse
from flask import Blueprint, request
from flask_cors import cross_origin
from .extensions import db
from .models import Note, Screenshot, Link


upload = Blueprint('upload', __name__, template_folder='templates')
# Routes

@upload.route("/delete_screenshot/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def delete_screenshot(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """

    # Process request (return dict)
    if request.method == "GET":
        screenshot = db.get_or_404(Screenshot, id)
        db.session.delete(screenshot)
        db.session.commit()
        return f"{id} has been deleted"

@upload.route("/update_screenshot/<id>", methods=["POST", "OPTIONS"])
@cross_origin()
def update_screenshot(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    # Process request (return dict)
    if request.method == "POST":

        screenshot = db.get_or_404(Screenshot, id)
        screenshot.caption = request_data["caption"]
        screenshot.text_in_image = request_data["text"]
        screenshot.about = request_data["about"]
        screenshot.date = request_data["date"]
        screenshot.view = request_data["view"]
        screenshot.related_activity = request_data["related_activity"]
        db.session.commit()
        return f"{id} has been updated"

@upload.route("/delete_note/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def delete_note(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """

    # Process request (return dict)
    if request.method == "GET":
        note = db.get_or_404(Note, id)
        db.session.delete(note)
        db.session.commit()
        return f"{id} has been deleted"

@upload.route("/update_note/<id>", methods=["POST", "OPTIONS"])
@cross_origin()
def update_note(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    # Process request (return dict)
    if request.method == "POST":

        note = db.get_or_404(Note, id)
        note.title = request_data["title"]
        note.about = request_data["about"]
        note.date = request_data["date"]
        note.view = request_data["view"]
        note.related_activity = request_data["related_activity"]
        db.session.commit()
        return f"{id} has been updated"

@upload.route("/delete_link/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def delete_link(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """

    # Process request (return dict)
    if request.method == "GET":
        link = db.get_or_404(Link, id)
        db.session.delete(link)
        db.session.commit()
        return f"{id} has been deleted"

@upload.route("/update_link/<id>", methods=["POST", "OPTIONS"])
@cross_origin()
def update_link(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = request.json

    # Process request (return dict)
    if request.method == "POST":

        link = db.get_or_404(Link, id)
        link.link = request_data["link"]
        link.about = request_data["about"]
        link.site_name = request_data["site_name"]
        link.date = request_data["date"]
        link.view = request_data["view"]
        link.related_activity = request_data["related_activity"]
        db.session.commit()
        return f"{id} has been updated"

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

        # Getting data from request and adding to the database.
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
            with current_app.app_context():
                if len(Link.query.filter_by(link=link).all()) == 0:
                    print("Query Link is not yet known, adding to database")
                    db.session.add(new_link)
                    db.session.commit()
                    new_links.append(new_dict_link)
                else:
                    print("Query Link is known")

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
        with current_app.app_context():
            if len(Note.query.filter_by(title=noteTitle).all()) == 0:
                print("Query Note is not yet known, adding to database and writing file")
                db.session.add(new_note)
                db.session.commit()

            response = jsonify([new_dict_note])
            return response
