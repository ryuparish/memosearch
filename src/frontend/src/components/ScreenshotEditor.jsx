import {
  useParams
} from "react-router-dom";
import React, { useContext, useState, useEffect } from 'react';
import { AppContext } from "../App";
import Button from "react-bootstrap/Button";
import { close_window, do_tab } from "./utils";


export default function ScreenshotEditor() {
  const {

  } = useContext(AppContext);

  const [caption, setCaption] = useState("");
  const [text, setText] = useState("");
  const [src, setSrc] = useState();
  const [view, setView] = useState("");
  const [about, setAbout] = useState("");
  const [date, setDate] = useState("");
  const [related_activity, setRelatedActivity] = useState("");

  const { Id } = useParams();

  const {
    setScreenshotError,
    screenshotError
  } = useContext(AppContext);

  

  useEffect(() => {
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/get_image/" + Id, {
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.blob();
      })
      .then((data) => {
        setSrc(data);
      })
      .catch((error) => console.log(error));
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/open_screenshot/" + Id, {
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the screenshot we got back in the editor (loading initial data with open_screenshot): " + JSON.stringify(data));
        setCaption(data.caption);
        setText(data.text);
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

    // Only allow database insertion on a screenshot that at least has
    // valid values
    setScreenshotError("")
    if (caption === "") {
      setScreenshotError("The caption of the screenshot is required")
    } else if (related_activity === "") {
      setScreenshotError("The activity of the screenshot is required")
    } else if (about === "") {
      setScreenshotError("The about of the screenshot is required")
    } else if (date === "") {
      setScreenshotError("The date of the screenshot is required")
    } else if (view === "") {
      setScreenshotError("The view of the screenshot is required")
    }

    if (screenshotError !== "") {
      return;
    }

    // Create a new screenshot formdata object and send to the server
    const screenshotObj = {
      about:about,
      related_activity:related_activity,
      caption:caption,
      text:text,
      date:date,
      view:view,
    }


    // Post to the "update_screenshot" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/update_screenshot/" + Id, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(screenshotObj)
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

    // Post to the "delete_screenshot" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/delete_screenshot/" + Id, {
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
      }) .catch((error) => console.log(error));
  }

  const image_src = src ? URL.createObjectURL(src) : "";

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
            <h1>Screenshot #{Id}, {related_activity}</h1>
          </div>
          <br />
          <form id="links">
            <h3> Update Screenshot </h3>
            <img src={image_src} alt="Image failed to load"/>
            <br/><br/>
              <label for="note">Text in image:</label>
            <input type="text" id="text_in_image" name="text_in_image" onChange={(e) => setText(e.target.value)} value={text}/><br/><br/>
              <label for="note">Caption:</label>
            <input type="text" id="caption" name="caption" onChange={(e) => setCaption(e.target.value)} value={caption}/><br/><br/>
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
            <Button style={{"float":"right"}} class="btn btn-danger" onClick={(e) => {
              handleDelete(e);
            }}>Delete</Button>
            <br /><br />
          </form>
        </div>
      </body>
    </div>
  )
}
