import React, { Component } from 'react';
import './App.css';

export default function App() {
  //const []
  return (
    <div>
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
      </head>
      <body>
        <div class="container">
          <div class="jumbotron">
            <h1>Memosearch</h1>
            <p>Search for links and screenshots</p>
          </div>
          <br/>
          <div class="row">
          <div class="col-xs-3">
            <img style={{"width":"30%"}}src="images/link.jpg"/>
            <br/>
            <button class="btn btn-info"><a style={{"color":"white"}} href="links.html">Links</a></button>
          </div>
          <div class="col-xs-3">
            <img style={{"width":"30%"}} src="images/screenshot.jpg"/>
            <br/>
            <button class="btn btn-info"><a style={{"color":"white"}} href="screenshots.html">Screenshots</a></button>
          </div>
          <div class="col-xs-3">
            <img style={{"width":"30%"}} src="images/notes.png"/>
            <br/>
            <button class="btn btn-info"><a style={{"color":"white"}} href="notes.html">Notes</a></button>
          </div>
          <div class="col-xs-3">
            <img style={{"width":"40%","padding":"5px"}} src="images/search.jpg"/>
            <br/>
            <button class="btn btn-warning"><a style={{"color":"white"}} href="search.html">Search</a></button>
          </div>
        </div>
      </div>
      </body>
    </div>

  )
  //return (
  //  <div className="App">
  //    <header className="App-header">
  //      <img src={logo} className="App-logo" alt="logo" />
  //      <p>
  //        Edit <code>src/App.js</code> and save to reload.
  //      </p>
  //      <a
  //        className="App-link"
  //        href="https://reactjs.org"
  //        target="_blank"
  //        rel="noopener noreferrer"
  //      >
  //        Learn React
  //      </a>
  //    </header>
  //  </div>
  //);
}
