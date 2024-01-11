import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams
} from "react-router-dom";
import React, { useContext, useState, useEffect } from 'react';
import { AppContext } from "../App";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import ViewModal from "./ViewModal";

export default function LinkEditor() {
  const {

  } = useContext(AppContext);

  const [link, setLink] = useState("");
  const [view, setView] = useState("");
  const [about, setAbout] = useState("");
  const [site_name, setSiteName] = useState("");
  const [date, setDate] = useState("");
  const [related_activity, setRelatedActivity] = useState("");

  const { Id } = useParams();

  const {
    setLinkError,
    linkError
  } = useContext(AppContext);



  useEffect(() => {
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/open_link/" + Id, {
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the link we got back in the editor (loading initial data with open_link): " + JSON.stringify(data));
        setLink(data.link);
        setAbout(data.about);
        setSiteName(data.site_name);
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

    // Only allow database insertion on a link that at least has
    // valid values
    setLinkError("")
    if (link === "") {
      setLinkError("The link of the link is required")
    } else if (related_activity === "") {
      setLinkError("The activity of the link is required")
    } else if (site_name === "") {
      setLinkError("The site_name of the link is required")
    } else if (about === "") {
      setLinkError("The about of the link is required")
    } else if (date === "") {
      setLinkError("The date of the link is required")
    } else if (view === "") {
      setLinkError("The view of the link is required")
    }

    if (linkError !== "") {
      return;
    }

    // Create a new link object and send to the server
    const linkObj = {
      about: about,
      related_activity: related_activity,
      link: link,
      site_name: site_name,
      date: date,
      view: view,
    }

    // Post to the "update_link" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/update_link/" + Id, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(linkObj)
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

    // Post to the "delete_link" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/delete_link/" + Id, {
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

	// Enable Tabs in the editor.
  function do_tab(e) {
		if (e.keyCode === 9) { // tab was pressed
			e.preventDefault();
      // get caret position/selection
      var val = e.target.value,
          start = e.target.selectionStart,
          end = e.target.selectionEnd;

      // set textarea value to: text before caret + tab + text after caret
      e.target.value = val.substring(0, start) + '\t' + val.substring(end);

      // put caret at right position again
      e.target.selectionStart = e.target.selectionEnd = start + 1;

      // prevent the focus lose
      return false;
    }
  }

  function close_window() {
    window.open('','_parent','');
    window.close();
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
            <h1>Link #{Id}, {related_activity}</h1>
          </div>
          <br />
          <form id="links">
            <h3> Update Link </h3><br />
            <label for="link">Visit&nbsp;</label>
            <a href={link}>{link}</a><br /><br />
            <label for="link">Link:</label>
            <input type="text" id="title" name="title" onChange={(e) => setLink(e.target.value)} value={link} /><br /><br />
            <label for="about">About:</label><br />
            <textarea id="about" name="freeform" rows="20" cols="100" onKeyDown={do_tab} onChange={(e) => setAbout(e.target.value)} value={about}></textarea><br /><br />
            <label for="activity">Related Activity:</label>
            <input type="text" id="activity" name="activity" onChange={(e) => setRelatedActivity(e.target.value)} value={related_activity} /><br /><br />
            <label for="link">View:</label>
            <input type="text" id="view" name="view" onChange={(e) => setView(e.target.value)} value={view} /><br /><br />
            <label for="date">Date:</label>
            <p>{date}</p><br />
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
