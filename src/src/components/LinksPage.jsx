import React, { useContext } from 'react';
import {AppContext} from "../App";

export default function LinksPage() {
  const [page, setPage] = useContext(AppContext);
  const date = new Date();
  const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
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
        <form id="links">
        <h3> Add Link </h3>
        <label for="link_name">Link name:</label>
          <input type="text" id="link_name" name="link_name"/><br/><br/>
        <label for="link">Link:</label>
          <input type="text" id="link" name="link"/><br/><br/>
        <label for="activity">Related Activity:</label>
          <input type="text" id="activity" name="activity"/><br/><br/>
        <label for="date">Date:</label>
        <input type="date" id="date" name="date" placeholder={formattedDate} disabled/><br/><br/>
        <label for="about">About:</label>
        <br/>
          <textarea id="about" name="freeform" rows="4" cols="50"></textarea><br/><br/>
          <button type="submit" class="btn btn-info" onClick={() => {}}>Submit</button>
        </form>
      </div>
    </body>
  </div>)
}
