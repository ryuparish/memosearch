import React, { useContext } from 'react';
import {AppContext} from "../App";
import LinkTable from "./LinkTable";

export default function LinksPage() {
  const {
    setPage,
    linkError,
  } = useContext(AppContext)

  return (
  <div>
    <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
      <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto|Varela+Round"/>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"/>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
      <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
    </head>
    
    <body>
      <div class="container">
        <br/><br/>
        <button class="btn btn-info" onClick={() => setPage("main")}>Back</button>
        <br/><br/>
        <div class="jumbotron">
          <h1>New Links</h1>
          <h2>Create a new link</h2>
        </div>
        <br/>
          <p><font color="red">{linkError}</font></p>
          <LinkTable/>
      </div>
    </body>
  </div>)
}
