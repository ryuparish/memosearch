from flask import jsonify
from flask import Blueprint, request, render_template
from flask_cors import cross_origin
from PIL import Image
from thefuzz import fuzz
from .models import Note, Screenshot, Link
from .app import db

retrieve = Blueprint('retrieve', __name__, template_folder='templates')

# Routes

@retrieve.route("/views", methods=["GET", "OPTIONS"])
@cross_origin()
def views():
    """Handles the link route.

    GET: This route gets information about the link
    and returns it in a dictionary.


    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    if request.method == "GET":
        all_views = set()
        all_views.add("all")
        for table in [Note, Link, Screenshot]:
            for value in table.query.distinct(table.view):
                print(value.view)
                all_views.add(value.view)
        return list(all_views)

@retrieve.route("/get_image/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def get_image(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """

    # Process request (return dict)
    if request.method == "GET":
        image_path = db.get_or_404(Screenshot, id).path
        file = Image.open(image_path)
        return file

@retrieve.route("/delete_link/<id>", methods=["GET", "OPTIONS"])
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

@retrieve.route("/update_link/<id>", methods=["POST", "OPTIONS"])
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


@retrieve.route("/open_link/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_link(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = Link.query.filter_by(id=id).one()

    # Process request (return dict)
    if request.method == "GET":
        print(f"Here is the request_data.view: {request_data.view}")
        return {
            "site_name": request_data.site_name,
            "about": request_data.about,
            "date": request_data.date,
            "link": request_data.link,
            "related_activity": request_data.related_activity,
            "id": request_data.id,
            "view": request_data.view,
        }

@retrieve.route("/open_screenshot/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_screenshot(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    print(f"Here is id in open_screenshot: {id}")
    request_data = Screenshot.query.filter_by(id=int(id)).one()

    # Process request (return dict)
    if request.method == "GET":
        return {
            "view": request_data.view,
            "about": request_data.about,
            "caption": request_data.caption,
            "text": request_data.text_in_image,
            "path": request_data.path,
            "date": request_data.date,
            "related_activity": request_data.related_activity,
            "id": request_data.id
        }

@retrieve.route("/open_note/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_note(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = Note.query.filter_by(id=id).one()

    # Process request (return dict)
    if request.method == "GET":
        return {
            "view": request_data.view,
            "title": request_data.title,
            "about": request_data.about,
            "date": request_data.date,
            "related_activity": request_data.related_activity,
            "id": request_data.id
        }

@retrieve.route("/topfive", methods=["GET", "OPTIONS"])
@cross_origin()
def topfive():
    top_5_links = Link.query.order_by(Link.date.desc()).limit(5).all()
    top_5_notes = Note.query.order_by(Note.date.desc()).limit(5).all()
    top_5_screenshots = Screenshot.query.order_by(Screenshot.date.desc()).limit(5).all()

    return {"links":top_5_links, "notes":top_5_notes, "screenshots":top_5_screenshots}


@retrieve.route("/search", methods=["POST", "OPTIONS"])
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
        print("curr_results: " + str(curr_results))
        print("request_data['search']: " + str(request_data["search"]))

        # Adding site-name-matched links to the result list
        if ("links" in request_data["content"]):
            all_links = Link.query.all() if request_data["view"] == "all" else Link.query.where(Link.view == request_data["view"])
            print(all_links)
            for link in all_links:
                token_set_score = fuzz.token_set_ratio(link.link, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.site_name, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.related_activity, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.view, request_data["search"]))
                print(f"links token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["links"] += [{
                        "id": link.id,
                        "about": link.about,
                        "link": link.link,
                        "site_name": link.site_name,
                        "related_activity": link.related_activity,
                        "view": link.view,
                    }]

        # Adding caption-matched screenshots to the result list
        if ("screenshots" in request_data["content"]):
            all_screenshots = Screenshot.query.all() if request_data["view"] == "all" else Screenshot.query.where(Screenshot.view == request_data["view"])
            for screenshot in all_screenshots:
                token_set_score = fuzz.token_set_ratio(screenshot.caption, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.text_in_image, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.related_activity, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.view, request_data["search"]))
                print(f"screenshots token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["screenshots"] += [{
                        "id": screenshot.id,
                        "about": screenshot.about,
                        "date": screenshot.date,
                        "path": screenshot.path,
                        "caption": screenshot.caption,
                        "text_in_image": screenshot.text_in_image,
                        "related_activity": screenshot.related_activity,
                        "view": screenshot.view,
                    }]

        # Adding title-matched notes to the result list
        if ("notes" in request_data["content"]):
            all_notes = Note.query.all() if request_data["view"] == "all" else Note.query.where(Note.view == request_data["view"])
            for note in all_notes:
                token_set_score = fuzz.token_set_ratio(note.title, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(note.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(note.related_activity, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(note.view, request_data["search"]))
                print(f"notes token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["notes"] += [{
                        "id": note.id,
                        "title": note.title,
                        "about": note.about,
                        "date": note.date,
                        "related_activity": note.related_activity,
                        "view": note.view,
                    }]

        response = jsonify(curr_results)
        print(curr_results)
        return response
