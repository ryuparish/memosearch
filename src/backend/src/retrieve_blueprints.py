from flask import jsonify
from flask import Blueprint, request, render_template
from flask_cors import cross_origin
from thefuzz import fuzz
from .models import Note, Screenshot, Link

retrieve = Blueprint('retrieve', __name__, template_folder='templates')

# Routes


@retrieve.route("/open_screenshot/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_screenshot(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = Screenshot.query.filter_by(id=id).one()
    path = str(request_data.id)

    # Process request (return html)
    if request.method == "GET":
        return render_template(
            "screenshot.html",
            path=path,
            about=request_data.about,
            date=request_data.date,
            text=request_data.text_in_image,
            caption=request_data.caption,
            related_activity=request_data.related_activity,
            content_type="Screenshot",
            content_id=request_data.id
        )


@retrieve.route("/open_note/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_note(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = Note.query.filter_by(id=id).one()

    # Process request (return html)
    if request.method == "GET":
        return render_template(
            "note.html",
            about=request_data.about,
            date=request_data.date,
            related_activity=request_data.related_activity,
            content_type="Note",
            content_id=request_data.id
        )


@retrieve.route("/open_link/<id>", methods=["GET", "OPTIONS"])
@cross_origin()
def open_link(id):
    """Handles the file obtaining route given an object.

    POST: This route returns an html page that has just text in it.

    :returns:   JSON representation of what was saved in database
    :rtype: list(dict (JSON))
    """
    request_data = Link.query.filter_by(id=id).one()

    # Process request (return html)
    if request.method == "GET":
        return render_template(
            "link.html",
            site_name=request_data.site_name,
            about=request_data.about,
            date=request_data.date,
            link=request_data.link,
            related_activity=request_data.related_activity,
            content_type="Link",
            content_id=request_data.id
        )

@retrieve.route("/topfive", methods=["GET", "OPTIONS"])
@cross_origin()
def topfive():
    top_5_links = Link.query.order_by(Link.date.desc()).limit(5).all()
    top_5_notes = Note.query.order_by(Note.date.desc()).limit(5).all()
    top_5_screenshots = Screenshot.query.order_by(Screenshot.date.desc()).limit(5).all()

    return [*top_5_links, *top_5_notes, *top_5_screenshots]


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
            all_links = Link.query.all()
            print(all_links)
            for link in all_links:
                token_set_score = fuzz.token_set_ratio(link.link, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.site_name, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(link.related_activity, request_data["search"]))
                print(f"links token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["links"] += [{
                        "id": link.id,
                        "about": link.about,
                        "link": link.link,
                        "site_name": link.site_name,
                        "related_activity": link.related_activity
                    }]

        # Adding caption-matched screenshots to the result list
        if ("screenshots" in request_data["content"]):
            all_screenshots = Screenshot.query.all()
            print(all_screenshots)
            for screenshot in all_screenshots:
                token_set_score = fuzz.token_set_ratio(screenshot.caption, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.text_in_image, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(screenshot.related_activity, request_data["search"]))
                print(f"screenshots token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["screenshots"] += [{
                        "id": screenshot.id,
                        "about": screenshot.about,
                        "date": screenshot.date,
                        "path": screenshot.path,
                        "caption": screenshot.caption,
                        "text_in_image": screenshot.text_in_image,
                        "related_activity": screenshot.related_activity
                    }]

        # Adding title-matched notes to the result list
        if ("notes" in request_data["content"]):
            all_notes = Note.query.all()
            print(all_notes)
            for note in all_notes:
                token_set_score = fuzz.token_set_ratio(note.title, request_data["search"])
                token_set_score = max(token_set_score, fuzz.token_set_ratio(note.about, request_data["search"]))
                token_set_score = max(token_set_score, fuzz.token_set_ratio(note.related_activity, request_data["search"]))
                print(f"notes token set score: {token_set_score}")
                if token_set_score > 50:
                    curr_results["notes"] += [{
                        "id": note.id,
                        "title": note.title,
                        "about": note.about,
                        "date": note.date,
                        "related_activity": note.related_activity
                    }]

        response = jsonify(curr_results)
        print(curr_results)
        return response
