import React, { useContext } from 'react';
import {AppContext} from "../App";

export default function LinksPage() {
  const {
    setPage,
    linkName,
    setLinkName,
    link,
    setLink,
    linkActivity,
    setLinkActivity,
    linkAbout,
    setLinkAbout,
    linkError,
    setLinkError,
  } = useContext(AppContext)


  // Handle the change of the react states
  function handleLinkChange(event) {
    setLink(event.target.value);
    var matches = event.target.value.match(/^https?\:\/\/([^/?#]+)(?:[/?#]|$)/i);
    var domain = matches && matches[1]; 
    // Set domain (site_name) only if there is a valid link
    if (domain) {
      setLinkName(matches[1]);
    } else {
      setLinkName("");
    }
  }

  const date = new Date();
  const formattedDate = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;
  
  // Get the submitted values and call the python backend
  // to create the database entry
  function handleSubmit(event) {
    event.preventDefault()

    // Only allow database insertion on a link that at least has
    // a link name
    setLinkError("")
    if (linkName === "") {
      setLinkError("The name of the link is required")
    } else if (link === "") {
      setLinkError("The link is required")
    } else if (linkActivity === "") {
      setLinkError("The activity of the link is required")
    } else if (linkAbout === "") {
      setLinkError("The about of the link is required")
    }

    if (linkError !== "") {
      return;
    }

    // Create a new link object and send to the server
    const linkObj = {
      linkName:linkName,
      link:link,
      linkActivity:linkActivity,
      linkAbout:linkAbout,
      linkDate:date
    }

    // Post to the "links" api
    fetch("http://127.0.0.1:4444/links", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(linkObj)
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the data we put into the database: " + JSON.stringify(data[0]));
      })
      .catch((error) => console.log(error));
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
        <button class="btn btn-info" onClick={() => setPage("main")}>Back</button>
        <div class="jumbotron">
          <h1>Configure Links</h1>
          <h2>Add, Delete, and Edit Link data</h2>
        </div>
        <br/>
        <form id="links" onSubmit={handleSubmit}>
        <h3> Add Link </h3>
        <label for="link_name">Link name:</label>
          <input type="text" id="link_name" name="link_name" value={linkName}/><br/><br/>
        <label for="link">Link:</label>
          <input type="text" id="link" name="link" onChange={handleLinkChange} value={link}/><br/><br/>
        <label for="activity">Related Activity:</label>
          <input type="text" id="activity" name="activity" onChange={(e) => setLinkActivity(e.target.value)} value={linkActivity}/><br/><br/>
        <label for="date">Date:</label>
          <p>{formattedDate}</p><br/>
        <label for="about">About:</label>
        <br/>
          <textarea id="about" name="about" rows="4" cols="50" onChange={(e) => setLinkAbout(e.target.value)} value={linkAbout}></textarea><br/><br/>
          <input type="submit" id="submit" name="submit"/>
        </form>
        <p><font color="red"> {linkError} </font></p>
      </div>
    </body>
  </div>)
}
