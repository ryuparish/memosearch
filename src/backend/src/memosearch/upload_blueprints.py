import os
import random
import json
from flask import jsonify, current_app
from urllib.parse import urlparse
from flask import Blueprint, request
from flask_cors import cross_origin
from .db import get_db
from dotenv import load_dotenv

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
        db = get_db()
        db.execute('''DELETE FROM "screenshots" WHERE id=?''', (id,))
        db.commit()
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

        print(request_data)
        db = get_db()
        db.execute(
            '''
            UPDATE "screenshots"
            SET caption=?, text_in_image=?, about=?, date=?, view=?, related_activity=?
            WHERE id=?
            ''',
            (
                request_data["caption"],
                request_data["text"],
                request_data["about"],
                request_data["date"],
                request_data["view"],
                request_data["related_activity"],
                id,
            )
        )
        db.commit()
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
        db = get_db()
        db.execute('''DELETE FROM "notes" WHERE id=?''', (id,))
        db.commit()
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

        db = get_db()
        db.execute(
            '''
            UPDATE "notes"
            SET title=?, about=?, date=?, view=?, related_activity=?
            WHERE id=?
            ''',
            (
                request_data["title"],
                request_data["about"],
                request_data["date"],
                request_data["view"],
                request_data["related_activity"],
                id,
            )
        )
        db.commit()
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
        db = get_db()
        db.execute('''DELETE FROM "links" WHERE id=?''', (id,))
        db.commit()
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

        db = get_db()
        db.execute(
            '''
            UPDATE "links"
            SET link=?, about=?, site_name=?, date=?, view=?, related_activity=?
            WHERE id=?
            ''',
            (
                request_data["link"],
                request_data["about"],
                request_data["site_name"],
                request_data["date"],
                request_data["view"],
                request_data["related_activity"],
                id,
            )
        )
        db.commit()
        print(f"{id} has been updated")
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
    db = get_db()
    print("HERE ERERERERERERERERERE1")
    request_form = request.form
    print("HERE ERERERERERERERERERE2")

    if request.method == "POST":
        # Check for empty screenshot
        if request.files["file"] is None or request.files["file"].filename == "":
            print("file is empty returning nothing")
            return "Error, file is empty"
        print("HERE ERERERERERERERERERE3")

        # Upload file to our directory
        id = random.getrandbits(16)
        target = os.environ.get("UPLOAD_FOLDER")
        if not os.path.isdir(target):
            os.mkdir(target)
        print("HERE ERERERERERERERERERE4")

        file = request.files['file']
        filename = str(id)
        destination = "/".join([target, filename])
        file.save(destination)
        print(f"HERE ERERERERERERERERERE5, destination: {destination}")

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

        print(f"Here is the caption in the code {request_form['caption']}")
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

        print("Here is the screenshot path: " + path)
        # Do not prevent duplicates
        db.execute("""
            INSERT INTO screenshots
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                id,
                caption,
                about,
                date,
                text_in_image,
                path,
                related_activity,
                view,
            )
        )
        db.commit()

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
    db = get_db()
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
            link_query = db.execute('SELECT * FROM links WHERE link = ?',(link,)).fetchall()
            if len(link_query) == 0:
                print("Query Link is not yet known, adding to database")
                db.execute(
                    '''
                    INSERT INTO links
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (id, link, about, date, site_name, related_activity, view,)
                )
                db.commit()
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
    db = get_db()
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
            note = db.execute(
                '''
                SELECT * FROM notes
                WHERE title=?
                ''',
                (noteTitle,)
            ).fetchall()

            if len(note) == 0:
                print("Query Note is not yet known, adding to database and writing file")
                db.execute("""
                    INSERT INTO notes
                    VALUES(?,?,?,?,?,?)
                    """,
                    (
                        id,
                        noteTitle,
                        about,
                        date,
                        related_activity,
                        view,
                    )
                )
                db.commit()

            response = jsonify([new_dict_note])
            return response
