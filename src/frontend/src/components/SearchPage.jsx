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
          <h1>Configure Screenshots</h1>
          <h2>Add, Delete, and Edit Screenshot data</h2>
        </div>
        <br/>
        <form id="links">
          <h3> Add Screenshot </h3>
            <label for="activity">File or Photo Directory:</label>
              <input type="file"/>
            <label for="Caption">Caption:</label>
              <input type="text" id="caption" name="caption"/><br/><br/>
            <label for="text_in_image">Text in image (if any):</label>
              <input type="text" id="text_in_image" name="text_in_image"/><br/><br/>
            <label for="activity">Related Activity:</label>
              <input type="text" id="activity" name="activity"/><br/><br/>
            <label for="date">Date:</label>
              <p>{formattedDate}</p><br/><br/>
            <label for="about">About:</label><br/>
              <textarea id="about" name="freeform" rows="4" cols="50"></textarea><br/><br/>
          <textarea id="about" name="freeform" rows="4" cols="50"></textarea><br/><br/>
          <button type="submit" class="btn btn-info" onClick={() => {}}>Submit</button>
        </form>
      </div>
    </body>
  </div>)
}
