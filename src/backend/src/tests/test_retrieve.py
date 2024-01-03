import json
import pytest
from memosearch import create_app


# Testing retrieval
@pytest.mark.parametrize(('search_content', 'view', 'search', 'count'), (
    (["links"], "all", "all", 1),
    (["screenshots"], "all", "all", 0),
    (["notes"], "all", "all", 2),
    (["links", "notes"], "random view1", "random view1", 2),
    (["links", "screenshots"], "random view3", "all", 0),
    (["notes", "screenshots"], "random view1", "bro2", 1),
    (["links", "screenshots", "notes"], "all",
     "somethingthatisdefinitelynotinthedatabasedude", 0),
))
def test_search(app, client, search_content, view, search, count):
    assert create_app({'TESTING': True}).testing

    search = {
        "content": search_content,
        "view": view,
        "search": search
    }

    response = client.post(
        "/search",
        content_type="application/json",
        data=json.dumps(search)
    ).json
    print(response)

    totalCount = 0
    for content in search_content:
        totalCount += len(response[content])

    assert totalCount == count


def test_notes_query(app, client):
    assert create_app({'TESTING': True}).testing

    # Retrieve existing note
    response = client.get('/open_note/3')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 3
    assert response.json["title"] == "random note1"
    assert response.json["about"] == "note bro1"
    assert response.json["date"] == "2024-03-02T02:46:36.013Z"
    assert response.json["related_activity"] == "writing note1"
    assert response.json["view"] == "all"


def test_screenshots_query(app, client):
    assert create_app({'TESTING': True}).testing

    # Retrieve existing note
    response = client.get('/open_screenshot/6')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 6
    assert response.json["caption"] == "screenshot1"
    assert response.json["about"] == "screenshot bro1"
    assert response.json["date"] == "2024-05-02T02:46:36.013Z"
    assert response.json["text"] == "screenshot text1"
    assert response.json["view"] == "random view2"


def test_links_query(app, client):
    assert create_app({'TESTING': True}).testing

    # Retrieve existing note
    response = client.get('/open_link/0')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 0
    assert response.json["link"] == "https://www.google.com/"
    assert response.json["about"] == "google bro1"
    assert response.json["date"] == "2024-01-02T02:46:36.013Z"
    assert response.json["site_name"] == "google.com"
    assert response.json["related_activity"] == "searching1"
    assert response.json["view"] == "random view1"


# Testing views

def test_views(app, client):
    assert create_app({'TESTING': True}).testing

    # Retrieve views
    response = client.get('/views')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(response.json) == 4
    assert response.json == ["all", "random view1",
                             "random view2", "random view3"]


def test_views_after_insert(app, client):
    # Insert a new link
    new_note = {
        "id": 11,
        "noteTitle": "some new title",
        "noteAbout": "some about text",
        "noteDate": "2023-01-09T02:46:36.013Z",
        "noteActivity": "some related activity",
        "view": "some view"
    }
    client.post(
        "/notes",
        content_type="application/json",
        data=json.dumps(new_note)
    )

    # Retrieve views
    response = client.get('/views')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(response.json) == 5
    assert response.json == ["all", "random view1",
                             "random view2", "random view3", "some view"]

# Testing topfive


def test_topfive(app, client):
    assert create_app({'TESTING': True}).testing

    # Retrieve views
    response = client.get('/topfive')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(response.json["links"]) == 3
    assert len(response.json["notes"]) == 3
    assert len(response.json["screenshots"]) == 3


def test_topfive_after_insertion(app, client):
    assert create_app({'TESTING': True}).testing

    new_note = {
        "id": 11,
        "noteTitle": "some new title",
        "noteAbout": "some about text",
        "noteDate": "2023-01-09T02:46:36.013Z",
        "noteActivity": "some related activity",
        "view": "some view"
    }
    response = client.post("/notes",
                           content_type="application/json",
                           data=json.dumps(new_note))

    # Retrieve views
    response = client.get('/topfive')
    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert len(response.json["links"]) == 3
    assert len(response.json["notes"]) == 4
    assert len(response.json["screenshots"]) == 3
