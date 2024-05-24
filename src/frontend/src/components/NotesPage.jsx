import React, { useContext } from 'react';
import {AppContext} from "../App";
import Button from "react-bootstrap/Button";
import { do_tab } from "./utils";

export default function NotesPage() {

  const {
    noteTitle,
    setNoteTitle,
    setPage,
    noteActivity,
    setNoteActivity,
    noteAbout,
    setNoteAbout,
    noteError,
    setNoteError,
    view
  } = useContext(AppContext);

  // Get current date and insert into input field.
  const date = new Date();
  const cleaned_date = date.toLocaleString();
  const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;

  // Get the submitted values and call the python backend
  // to create the database entry
  function handleSubmit(event) {
    event.preventDefault()

    // Only allow database insertion on a note that at least has
    // valid values
    setNoteError("")
    if (noteTitle === "") {
      setNoteError("The title of the note is required")
    } else if (noteActivity === "") {
      setNoteError("The activity of the note is required")
    } else if (noteAbout === "") {
      setNoteError("The about of the note is required")
    }

    if (noteError !== "") {
      return;
    }

    // Create a new note object and send to the server
    const noteObj = {
      noteTitle:noteTitle,
      noteActivity:noteActivity,
      noteAbout:noteAbout,
      noteDate:cleaned_date,
      view:view,
      description_string:noteAbout.slice(0,150) + " " + noteActivity + " " + view,
    }

    // Post to the "notes" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/notes", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(noteObj)
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the data we put into the database: " + JSON.stringify(data[0]));
      })
      .catch((error) => console.log(error));
    setPage("main");
  }

  function handleClear () {
    setNoteAbout("");
    setNoteTitle("");
    setNoteActivity("");
  }

  return (
  <div>
    <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
      <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
    </head>
    
    <body>
      <br/>
      <div class="container">
        <br/><br/>
        <button class="btn btn-info" onClick={() => setPage("main")}>Back</button>
        <br/><br/>
        <div class="jumbotron">
          <h1>Note</h1>
          <h2>Create a new note</h2>
        </div>
        <br/>
        <form id="links">
          <h3> New Note </h3>
            <label for="title">Title:</label>
          <input type="text" id="title" name="title" onChange={(e) => setNoteTitle(e.target.value)} value={noteTitle}/><br/><br/>
            <label for="about">About:</label><br/>
          <textarea id="about" name="freeform" rows="20" cols="100" onKeyDown={do_tab} onChange={(e) => setNoteAbout(e.target.value)} value={noteAbout}></textarea><br/><br/>
            <label for="activity">Related Activity:</label>
          <input type="text" id="activity" name="activity" onChange={(e) => setNoteActivity(e.target.value)} value={noteActivity}/><br/><br/>
            <label for="date">Date:</label>
              <p>{formattedDate}</p><br/>
          <Button type="submit" class="btn btn-info" onClick={(e) => handleSubmit(e)}>Submit</Button>
          &nbsp;&nbsp;
          <Button class="btn btn-info" onClick={handleClear}>Clear</Button>
        </form>
        <p><font color="red"> {noteError} </font></p>
      </div>
    </body>
  </div>)
}
