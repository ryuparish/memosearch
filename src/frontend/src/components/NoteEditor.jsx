import {
  BrowserRouter as Router,
  useParams
} from "react-router-dom";
import React, { useContext, useState, useEffect } from 'react';
import { AppContext } from "../App";
import Button from "react-bootstrap/Button";
import { close_window, do_tab } from "./utils";

export default function NoteEditor() {
  const {

  } = useContext(AppContext);

  const [title, setTitle] = useState("");
  const [view, setView] = useState("");
  const [about, setAbout] = useState("");
  const [date, setDate] = useState("");
  const [related_activity, setRelatedActivity] = useState("");

  const { Id } = useParams();

  const {
    setNoteError,
    noteError
  } = useContext(AppContext);

  

  useEffect(() => {
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/open_note/" + Id, {
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the note we got back in the editor (loading initial data with open_note): " + JSON.stringify(data));
        setTitle(data.title);
        setAbout(data.about);
        setDate(data.date);
        setRelatedActivity(data.related_activity);
        setView(data.view);
      })
      .catch((error) => console.log(error));
  }, [])


  // Get the submitted values and call the python backend
  // to create the database entry
  function handleSubmit(event) {
    event.preventDefault()

    // Only allow database insertion on a note that at least has
    // valid values
    setNoteError("")
    if (title === "") {
      setNoteError("The title of the note is required")
    } else if (related_activity === "") {
      setNoteError("The activity of the note is required")
    } else if (about === "") {
      setNoteError("The about of the note is required")
    } else if (date === "") {
      setNoteError("The date of the note is required")
    } else if (view === "") {
      setNoteError("The view of the note is required")
    }

    if (noteError !== "") {
      return;
    }

    // Create a new note object and send to the server
    const noteObj = {
      about:about,
      related_activity:related_activity,
      title:title,
      date:date,
      view:view,
    }

    // Post to the "update_note" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/update_note/" + Id, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(noteObj)
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        close_window();
      })
      .catch((error) => console.log(error));
  }



  // Get the submitted values and call the python backend
  // to create the database entry
  function handleDelete(event) {
    event.preventDefault()

    // Post to the "delete_note" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/delete_note/" + Id, {
      method: "GET",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        close_window();
      })
      .catch((error) => console.log(error));
  }


  return (
    <div>
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
      </head>
      <body>
        <div class="container">
          <br />
          <Button type="submit" class="btn btn-dark" onClick={close_window}>Close</Button>
          <br /><br />
          <div class="jumbotron">
            <h1>Note #{Id}, {related_activity}</h1>
          </div>
          <br />
          <form id="links">
            <h3> Update Note </h3>
              <label for="note">Title:</label>
            <input type="text" id="title" name="title" onChange={(e) => setTitle(e.target.value)} value={title}/><br/><br/>
              <label for="about">About:</label><br/>
            <textarea id="about" name="freeform" rows="20" cols="100" onChange={(e) => setAbout(e.target.value)} onKeyDown={do_tab} value={about}></textarea><br/><br/>
              <label for="activity">Related Activity:</label>
            <input type="text" id="activity" name="activity" onChange={(e) => setRelatedActivity(e.target.value)} value={related_activity}/><br/><br/>
              <label for="view">View:</label>
            <input type="text" id="view" name="view" onChange={(e) => setView(e.target.value)} value={view}/><br/><br/>
              <label for="date">Date:</label>
                <p>{date}</p><br/>
            <Button type="submit" class="btn btn-info" onClick={(e) => handleSubmit(e)}>Update</Button>
            &nbsp;&nbsp;
            <Button style={{"float":"right"}}class="btn btn-danger" onClick={(e) => {
              handleDelete(e);
            }}>Delete</Button>
            <br /><br />
          </form>
        </div>
      </body>
    </div>
  )
}
