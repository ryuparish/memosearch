import React, { useContext } from 'react';
import {AppContext} from "../App";
import LinkTable from "./LinkTable";

export default function LinkExperiment() {
  const {
    setPage,
    linkError,
  } = useContext(AppContext)

  console.log("IN HERE THOUGH")
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
      <br/>
      <div class="container">
        <button class="btn btn-info" onClick={() => setPage("main")}>Back</button>
        <div class="jumbotron">
          <h1>Configure Links</h1>
          <h2>Add, Delete, and Edit Link data</h2>
        </div>
        <br/>
          <LinkTable/>
          <p><font color="red"> {linkError} </font></p>
      </div>
    </body>
  </div>)
}
