from memosearch import create_app
from memosearch.db import get_db
import os
import json
import pytest
import sqlite3


# Test sqlite3 execution


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # This means that the error did not trigger and was closed
    assert 'closed' in str(e.value)


# Testing insertion


def test_notes_insertion(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new note
    new_note = {
        "id": 11,
        "noteTitle": "some new title",
        "noteAbout": "some about text",
        "noteDate": "2023-01-09T02:46:36.013Z",
        "noteActivity": "some related activity",
        "view": "some view"
    }
    generated_id = client.post(
        "/notes",
        content_type="application/json",
        data=json.dumps(new_note)
    ).json[0]["id"]

    response = client.get(f'/open_note/{generated_id}')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == generated_id
    assert response.json["about"] == "some about text"
    assert response.json["title"] == "some new title"
    assert response.json["date"] == "2023-01-09T02:46:36.013Z"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_link_insertion(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    new_link = {
        "id": 11,
        "link": "https://www.google.com/something",
        "about": "some about text",
        "date": "2023-01-02T02:46:36.013Z",
        "site_name": "google.com",
        "related_activity": "some related activity",
        "view": "some view"
    }

    # Get generated id and check information
    generated_id = client.post(
        "/links",
        content_type="application/json",
        data=json.dumps([new_link])
    ).json[0]["id"]

    response = client.get(f'/open_link/{generated_id}')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == generated_id
    assert response.json["link"] == "https://www.google.com/something"
    assert response.json["about"] == "some about text"
    assert response.json["date"] == "2023-01-02T02:46:36.013Z"
    assert response.json["site_name"] == "google.com"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_screenshot_insertion(app, client):
    assert create_app({'TESTING': True}).testing


    # Insert a new screenshot
    image = os.getenv("IMAGE_FILE")
    new_screenshot = {
        "about": "something",
        "caption": "some caption",
        "date": "2023-01-07T02:46:36.013Z",
        "text": "some text",
        "path": "",
        "activity": "some related activity",
        "view": "some view",
        "file": (open(image, "rb"), image)
    }

    # Get generated id and check information
    generated_id = client.post(
        "/screenshots",
        content_type="multipart/form-data",
        follow_redirects=True,
        data=new_screenshot
    ).json[0]["id"]

    response = client.get(f'/open_screenshot/{generated_id}')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == generated_id
    assert response.json["about"] == "something"
    assert response.json["caption"] == "some caption"
    assert response.json["date"] == "2023-01-07T02:46:36.013Z"
    assert response.json["text"] == "some text"
    assert response.json["path"] != ("" or None)
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


# Testing updates


def test_notes_update(app, client):
    assert create_app({'TESTING': True}).testing

    # Update a note
    new_note = {
        "id": 3,
        "title": "some updated title",
        "about": "some about text",
        "date": "2023-01-09T02:46:36.013Z",
        "related_activity": "some related activity",
        "view": "some view"
    }

    client.post(
        "/update_note/3",
        content_type="application/json",
        data=json.dumps(new_note)
    )

    response = client.get("/open_note/3")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 3
    assert response.json["about"] == "some about text"
    assert response.json["title"] == "some updated title"
    assert response.json["date"] == "2023-01-09T02:46:36.013Z"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_link_update(app, client):
    assert create_app({'TESTING': True}).testing

    # Update a link
    new_link = {
        "id": 0,
        "link": "https://www.google.com/something_else",
        "about": "some about text",
        "date": "2023-01-02T02:46:36.013Z",
        "site_name": "google.com",
        "related_activity": "some new related activity",
        "view": "some view"
    }

    client.post(
        "/update_link/0",
        content_type="application/json",
        data=json.dumps(new_link)
    )

    response = client.get("/open_link/0")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 0
    assert response.json["link"] == "https://www.google.com/something_else"
    assert response.json["about"] == "some about text"
    assert response.json["date"] == "2023-01-02T02:46:36.013Z"
    assert response.json["site_name"] == "google.com"
    assert response.json["related_activity"] == "some new related activity"
    assert response.json["view"] == "some view"


def test_screenshot_update(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            '''
            UPDATE "screenshots"
            SET caption=?, about=?, date=?, text_in_image=?, path=?, related_activity=?, view=?
            WHERE id=?
            ''',
            (
                "some new caption",
                "something",
                "2023-01-07T02:46:36.013Z",
                "some text",
                "some path",
                "some related activity",
                "some view",
                6,
            )
        )
        db.commit()

    response = client.get('/open_screenshot/6')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 6
    assert response.json["about"] == "something"
    assert response.json["caption"] == "some new caption"
    assert response.json["date"] == "2023-01-07T02:46:36.013Z"
    assert response.json["text"] == "some text"
    assert response.json["path"] == "some path"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


# Testing deletion


def test_notes_deletion(app, client):
    assert create_app({'TESTING': True}).testing

    # Ensure note was there before deletion
    assert client.get('/open_note/3').status_code == 200

    # Delete a note
    client.get("/delete_note/3")

    # Check that it is now gone
    with pytest.raises(TypeError) as excinfo:
        client.get('/open_note/3')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"


def test_link_deletion(app, client):
    assert create_app({'TESTING': True}).testing

    # Ensure link was there before deletion
    assert client.get('/open_link/0').status_code == 200

    # Delete a link
    client.get("/delete_link/0")

    # Check for deleted link
    with pytest.raises(TypeError) as excinfo:
        client.get('/open_link/0')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"


def test_screenshot_deletion(app, client):
    assert create_app({'TESTING': True}).testing

    # Ensure screenshot was there before deletion
    assert client.get('/open_screenshot/6').status_code == 200

    # Delete a screenshot
    client.get("/delete_screenshot/6")

    # Check for deleted screenshot
    with pytest.raises(TypeError) as excinfo:
        client.get('/open_screenshot/6')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"
