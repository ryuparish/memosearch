import os
import random
from flask import jsonify, current_app
from flask import Blueprint, request
from flask_cors import cross_origin
from .db import get_db
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

upload = Blueprint('upload', __name__, template_folder='templates')
# Routes


@upload.route("/delete_screenshot/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def delete_screenshot(id):
    """
    delete_screenshot(id)
    Handles deleting a screenshot with the given screenshot id. This route deletes the screenshot data of the screenshot with the given id.

    :param id: The corresponding id to the screenshot we want to delete.
    :type: int
    :returns: String that shows the successful delete message.
    :rtype: str
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
    """Handles updating a screenshot with the given screenshot id.
    This route updates the screenshot data of the screenshot with the given id.

    :param id: The corresponding id to the screenshot we want to update.
    :type: int
    :returns: String that shows the successful update message.
    :rtype: str
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
    """Handles deleting a note with the given note id.
    This route deletes the note data of the note with the given id.

    :param id: The corresponding id to the note we want to delete.
    :type: int
    :returns: String that shows the successful delete message.
    :rtype: str
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
    """Handles updating a note with the given note id.
    This route updates the note data of the note with the given id.

    :param id: The corresponding id to the note we want to update.
    :type: int
    :returns: String that shows the successful update message.
    :rtype: str
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
    """Handles deleting a link with the given link id.
    This route deletes the link data of the link with the given id.

    :param id: The corresponding id to the link we want to delete.
    :type: int
    :returns: String that shows the successful delete message.
    :rtype: str
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
    """Handles updating a link with the given link id.
    This route updates the link data of the link with the given id.

    :param id: The corresponding id to the link we want to update.
    :type: int
    :returns: String that shows the successful update message.
    :rtype: str
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
        return f"{id} has been updated"


@upload.route("/screenshots", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def screenshots():
    """Handles the screenshot route.
    GET: This route gets information about the screenshot
    and returns it in a dictionary.
    POST: This route adds information about the given screenshot
    and returns the result in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    db = get_db()
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
        description_string = request_form["description_string"]

        new_dict_screenshot = {
            "id": id,
            "about": about,
            "caption": caption,
            "date": date,
            "text_in_image": text_in_image,
            "path": path,
            "related_activity": related_activity,
            "view": view,
            "description_string": description_string,
        }

        # Do not prevent duplicates
        save_vector(new_dict_screenshot, "screenshot")
        db.execute("""
            INSERT INTO screenshots
            VALUES(?,?,?,?,?,?,?,?,?)
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
                       description_string,
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
            description_string = f"{about[:150]} {related_activity} {view}"

            # Getting data from json and adding to the database.
            new_dict_link = {
                "id": id,
                "link": link,
                "about": about,
                "date": date,
                "site_name": site_name,
                "related_activity": related_activity,
                "view": view,
                "description_string": description_string,
            }

            # Prevent duplicates
            link_query = db.execute(
                'SELECT * FROM links WHERE link = ?', (link,)).fetchall()
            if len(link_query) == 0:
                print("Query Link is not yet known, adding to database")
                save_vector(new_dict_link, "link")
                db.execute(
                    '''
                    INSERT INTO links
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (id, link, about, date, site_name, related_activity, view, description_string,)
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
            return f"Error, note title is empty: {request_data['noteTitle']}"

        # Data for database.
        id = random.getrandbits(16)
        noteTitle = request_data["noteTitle"]
        about = request_data["noteAbout"]
        date = request_data["noteDate"]
        related_activity = request_data["noteActivity"]
        view = request_data["view"]
        description_string = request_data["description_string"]

        # Getting data from request and adding to the database.
        new_dict_note = {
            "id": id,
            "title": noteTitle,
            "about": about,
            "date": date,
            "related_activity": related_activity,
            "view": view,
            "description_string": description_string,
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
                save_vector(new_dict_note, "note")
                db.execute("""
                    INSERT INTO notes
                    VALUES(?,?,?,?,?,?,?)
                    """,
                           (
                               id,
                               noteTitle,
                               about,
                               date,
                               related_activity,
                               view,
                               description_string,
                           )
                           )
                db.commit()
            else:
                print("Query Note already seen before")

            response = jsonify([new_dict_note])
            return response

def save_vector(memo, memo_type):
    """Saves the given memo into the vector database with the given id if not yet saved.

    :param memo: the memo we want to encode and save
    :type: JSON
    :param memotype: The corresponding memotype (note,ss,link) to the memo we want to encode.
    :type: str
    :raises ValueError: Invalid memo_type option from the below list
    :returns: None
    """
    memotypes = ["note", "screenshot", "link"]

    # Checking for correct memo type given
    if memo_type not in memotypes:
        raise ValueError(f"Invalid memo type: {memo_type}")

    # Combine data into description string then check
    # Note: In order for matches to work, we need content about the memo in the vector.

    # Checking if we have the same description_string
    db = get_db()
    matching_dstrings = db.execute(
        """SELECT description_string FROM notes
        WHERE description_string=?
        UNION
        SELECT description_string FROM links
        WHERE description_string=?
        UNION
        SELECT description_string FROM screenshots
        WHERE description_string=?""", (memo['description_string'], memo['description_string'], memo['description_string'],)
    ).fetchall()

    # If the description_string exists
    if len(matching_dstrings) > 0:
        print(f"We looked to check for a duplicate of this: {memo['description_string']}")
        print(f"matching database entry was found, no vector created: {matching_dstrings[0]['description_string']}")
        return

    # If the description_string does not exist
    # Loading faiss index if it exists
    if os.path.isfile("/Users/ryuparish/Code/memosearch/src/backend/src/instance/faiss.index"):
        faiss_index = faiss.read_index("/Users/ryuparish/Code/memosearch/src/backend/src/instance/faiss.index")

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        sentence_embedding = model.encode(memo['description_string'])
        print(f"The size of the index before is: {faiss_index.ntotal}")
        print(f"Id is of type: {type(id)}")
        faiss_index.add_with_ids(np.array([sentence_embedding]), np.array([memo["id"]]))
        print(f"The size of the index after is: {faiss_index.ntotal}")
        faiss.write_index(faiss_index, "/Users/ryuparish/Code/memosearch/src/backend/src/instance/faiss.index")
    else:
        print("Faiss file could be found on the python backend.")

