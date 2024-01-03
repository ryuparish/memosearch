from memosearch import create_app
from memosearch.db import get_db
import sys
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

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            """
            INSERT INTO notes
            VALUES(?,?,?,?,?,?)
            """,
            (
                10,
                "some title",
                "some about text",
                "2023-01-09T02:46:36.013Z",
                "some related activity",
                "some view",
            )
        )
        db.commit()

    response = client.get('/open_note/10')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 10
    assert response.json["about"] == "some about text"
    assert response.json["title"] == "some title"
    assert response.json["date"] == "2023-01-09T02:46:36.013Z"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_link_insertion(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            """
            INSERT INTO links
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                10,
                "https://www.google.com/",
                "some about text",
                "2023-01-02T02:46:36.013Z",
                "google.com",
                "some related activity",
                "some view",
            )
        )
        db.commit()

    response = client.get('/open_link/10')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 10
    assert response.json["link"] == "https://www.google.com/"
    assert response.json["about"] == "some about text"
    assert response.json["date"] == "2023-01-02T02:46:36.013Z"
    assert response.json["site_name"] == "google.com"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_screenshot_insertion(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            """
            INSERT INTO screenshots
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                10,
                "some caption",
                "something",
                "2023-01-07T02:46:36.013Z",
                "some text",
                "some path",
                "some related activity",
                "some view",
            )
        )
        db.commit()

    response = client.get('/open_screenshot/10')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 10
    assert response.json["about"] == "something"
    assert response.json["caption"] == "some caption"
    assert response.json["date"] == "2023-01-07T02:46:36.013Z"
    assert response.json["text"] == "some text"
    assert response.json["path"] == "some path"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


# Testing updates


def test_notes_update(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            '''
            UPDATE "notes"
            SET title=?, about=?, date=?, view=?, related_activity=?
            WHERE id=?
            ''',
            (
                "some new title",
                "some about text",
                "2023-01-09T02:46:36.013Z",
                "some view",
                "some related activity",
                3,
            )
        )
        db.commit()

    response = client.get('/open_note/3')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 3
    assert response.json["about"] == "some about text"
    assert response.json["title"] == "some new title"
    assert response.json["date"] == "2023-01-09T02:46:36.013Z"
    assert response.json["related_activity"] == "some related activity"
    assert response.json["view"] == "some view"


def test_link_update(app, client):
    assert create_app({'TESTING': True}).testing

    # Insert a new link
    with app.app_context():
        db = get_db()
        db.execute(
            '''
            UPDATE "links"
            SET link=?, about=?, date=?, site_name=?, related_activity=?, view=?
            WHERE id=?
            ''',
            (
                "https://www.google.com/",
                "some about text",
                "2023-01-02T02:46:36.013Z",
                "google.com",
                "some new related activity",
                "some view",
                0,
            )
        )
        db.commit()

    response = client.get('/open_link/0')

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.json["id"] == 0
    assert response.json["link"] == "https://www.google.com/"
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
        response = client.get('/open_note/3')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"

def test_link_deletion(app, client):
    assert create_app({'TESTING': True}).testing

    # Ensure link was there before deletion
    assert client.get('/open_link/0').status_code == 200

    # Delete a link
    client.get("/delete_link/0")

    # Check for deleted link
    with pytest.raises(TypeError) as excinfo:
        response = client.get('/open_link/0')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"


def test_screenshot_deletion(app, client):
    assert create_app({'TESTING': True}).testing

    # Ensure screenshot was there before deletion
    assert client.get('/open_screenshot/6').status_code == 200

    # Delete a screenshot
    client.get("/delete_screenshot/6")

    # Check for deleted screenshot
    with pytest.raises(TypeError) as excinfo:
        response = client.get('/open_screenshot/6')

    assert str(excinfo.value) == "'NoneType' object is not subscriptable"
