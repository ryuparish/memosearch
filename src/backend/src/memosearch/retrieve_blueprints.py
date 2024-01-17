import os
from flask import jsonify, send_file
from flask import Blueprint, request
from flask_cors import cross_origin
from PIL import Image
from thefuzz import fuzz
from .db import get_db

retrieve = Blueprint('retrieve', __name__, template_folder='templates')

# Routes


@retrieve.route("/views", methods=["GET", "OPTIONS"])
@cross_origin()
def views():
    """Handles the views route.

    GET: This route gets all views and returns them in a sorted list.


    :returns: List of strings that represent the views in the database.
    :rtype: list(str)
    """
    if request.method == "GET":
        all_views = set()
        all_views.add("all")
        db = get_db()
        uniq_views = db.execute(
            'SELECT view FROM notes '
            'UNION '
            'SELECT view FROM links '
            'UNION '
            'SELECT view FROM screenshots'
        ).fetchall()
        uniq_views = [row["view"] for row in uniq_views]
        all_views = all_views.union(set(uniq_views))
        return sorted(list(all_views))


@retrieve.route("/get_image/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def get_image(id):
    """Handles obtaining the image data from the saved directory when loading screenshot data.

    GET: This route returns a jpeg image (700, 700) corresponding to the given screenshot id.

    :param id int: screenshot id
    :returns: jpeg file
    :rtype: bytes
    """

    # Process request (return dict)
    if request.method == "GET":
        db = get_db()
        image_path = db.execute(
            '''SELECT * FROM "screenshots" WHERE id=?''', (id,)).fetchone()["path"]
        file = Image.open(image_path)
        if os.path.splitext(image_path):
            new_image = file.resize((700, 700))
            if new_image.mode in ("RGBA", "P"):
                new_image = new_image.convert("RGB")
            new_image.save(image_path + ".jpeg")
            image_path = image_path + ".jpeg"
        return send_file(image_path, mimetype="image/jpeg")


@retrieve.route("/open_link/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_link(id):
    """Returns link information with the given id number.

    GET: This route returns link information to display for link data.

    :param id int: link id
    :returns:   JSON representation of what link was saved in database
    :rtype: dict (JSON)
    """
    db = get_db()
    request_data = db.execute(
        '''SELECT * FROM "links" WHERE id=?''', (id,)).fetchone()

    # Process request (return dict)
    if request.method == "GET":
        return {
            "site_name": request_data["site_name"],
            "about": request_data["about"],
            "date": request_data["date"],
            "link": request_data["link"],
            "related_activity": request_data["related_activity"],
            "id": request_data["id"],
            "view": request_data["view"],
        }


@retrieve.route("/open_screenshot/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_screenshot(id):
    """Returns screenshot information with the given id number.

    GET: This route returns screenshot information to display for screenshot data.

    :param id int: screenshot id
    :returns:   JSON representation of what screenshot was saved in database
    :rtype: dict (JSON)
    """
    db = get_db()
    request_data = db.execute(
        '''SELECT * FROM "screenshots" WHERE id=?''', (id,)).fetchone()

    # Process request (return dict)
    if request.method == "GET":
        return {
            "view": request_data["view"],
            "caption": request_data["caption"],
            "text": request_data["text_in_image"],
            "path": request_data["path"],
            "about": request_data["about"],
            "date": request_data["date"],
            "related_activity": request_data["related_activity"],
            "id": request_data["id"]
        }


@retrieve.route("/open_note/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_note(id):
    """Returns note information with the given id number.

    GET: This route returns note information to display for note data.

    :param id int: note id
    :returns:   JSON representation of what note was saved in database
    :rtype: dict (JSON)
    """
    db = get_db()
    request_data = db.execute(
        '''SELECT * FROM "notes" WHERE id=?''', (id,)).fetchone()

    # Process request (return dict)
    if request.method == "GET":
        return {
            "view": request_data["view"],
            "title": request_data["title"],
            "about": request_data["about"],
            "date": request_data["date"],
            "related_activity": request_data["related_activity"],
            "id": request_data["id"]
        }


@retrieve.route("/topfive", methods=["GET", "OPTIONS"])
@cross_origin()
def topfive():
    """Returns top five most recent links, notes, and screenshot.

    GET: This route returns top five items of each content type.

    :returns:   JSON with each content type mapped to it's top five most recent items
    :rtype: dict (JSON)
    """
    db = get_db()

    top_5_notes = db.execute(
        '''SELECT * FROM "notes" ORDER BY date DESC LIMIT 10''').fetchall() or []
    top_5_notes_parsed = []
    for note in top_5_notes:
        new_addition = {}
        for key in note.keys():
            new_addition[key] = note[key]
        top_5_notes_parsed.append(new_addition)

    top_5_notes = {key: note[key]
                   for note in top_5_notes for key in note.keys()}

    top_5_links = db.execute(
        '''SELECT * FROM "links" ORDER BY date DESC LIMIT 10''').fetchall() or []
    top_5_links_parsed = []
    for link in top_5_links:
        new_addition = {}
        for key in link.keys():
            new_addition[key] = link[key]
        top_5_links_parsed.append(new_addition)

    top_5_links = {key: link[key]
                   for link in top_5_links for key in link.keys()}

    top_5_screenshots = db.execute(
        '''SELECT * FROM "screenshots" ORDER BY date DESC LIMIT 10''').fetchall() or []
    top_5_screenshots_parsed = []
    for screenshot in top_5_screenshots:
        new_addition = {}
        for key in screenshot.keys():
            new_addition[key] = screenshot[key]
        top_5_screenshots_parsed.append(new_addition)

    res = {"links": top_5_links_parsed, "notes": top_5_notes_parsed,
           "screenshots": top_5_screenshots_parsed}

    return res


@retrieve.route("/search", methods=["POST", "OPTIONS"])
@cross_origin()
def search():
    """Handles the search route.

    POST: This route returns all the matching results from the query.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    db = get_db()
    request_data = request.json

    # Process request (return list of dicts)
    if request.method == "POST":
        curr_results = {k: [] for k in request_data["content"]}

        # Adding site-name-matched links to the result list
        if ("links" in request_data["content"]):
            all_links = []
            if request_data["view"] == "all":
                all_links = db.execute(
                    '''SELECT * FROM "links"'''
                )
            else:
                all_links = db.execute(
                    '''SELECT * FROM "links" WHERE view = ?''',
                    (request_data["view"],)
                )
            for link in all_links:
                token_set_score = fuzz.token_set_ratio(
                    link["link"], request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    link["about"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    link["site_name"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    link["related_activity"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    link["view"], request_data["search"]))
                if token_set_score > 50:
                    curr_results["links"] += [{
                        "id": link["id"],
                        "about": link["about"],
                        "link": link["link"],
                        "site_name": link["site_name"],
                        "related_activity": link["related_activity"],
                        "view": link["view"],
                    }]

        # Adding caption-matched screenshots to the result list
        if ("screenshots" in request_data["content"]):
            all_screenshots = []

            if request_data["view"] == "all":
                all_screenshots = db.execute(
                    '''SELECT * FROM "screenshots"'''
                )

            else:
                all_screenshots = db.execute(
                    '''SELECT * FROM "screenshots" WHERE view = ?''',
                    (request_data["view"],)
                )

            for screenshot in all_screenshots:
                token_set_score = fuzz.token_set_ratio(
                    screenshot["caption"], request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    screenshot["about"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    screenshot["text_in_image"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    screenshot["related_activity"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    screenshot["view"], request_data["search"]))
                if token_set_score > 50:
                    curr_results["screenshots"] += [{
                        "id": screenshot["id"],
                        "about": screenshot["about"],
                        "date": screenshot["date"],
                        "path": screenshot["path"],
                        "caption": screenshot["caption"],
                        "text_in_image": screenshot["text_in_image"],
                        "related_activity": screenshot["related_activity"],
                        "view": screenshot["view"],
                    }]

        # Adding title-matched notes to the result list
        if ("notes" in request_data["content"]):
            all_notes = []
            if request_data["view"] == "all":
                all_notes = db.execute(
                    'SELECT * FROM notes'
                )
            else:
                all_notes = db.execute(
                    '''
                    SELECT * FROM notes
                    WHERE view=?
                    ''',
                    (request_data["view"],)
                )
            for note in all_notes:
                token_set_score = fuzz.token_set_ratio(
                    note["title"], request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    note["about"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    note["related_activity"], request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(
                    note["view"], request_data["search"]))
                if token_set_score > 50:
                    curr_results["notes"] += [{
                        "id": note["id"],
                        "title": note["title"],
                        "about": note["about"],
                        "date": note["date"],
                        "related_activity": note["related_activity"],
                        "view": note["view"],
                    }]

        response = jsonify(curr_results)
        return response
