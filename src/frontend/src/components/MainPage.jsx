import React, { useContext } from 'react';
import link_image from "../images/link.jpg";
import screenshot_image from "../images/screenshot.jpg";
import notes_image from "../images/notes.png";
import { AppContext } from "../App";
import SearchBar from "./SearchBar";
import SearchResults from "./SearchResults";
import "./style.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import ViewModal from "./ViewModal";
import Row from 'react-bootstrap/Row';
import Badge from 'react-bootstrap/Badge';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import ViewDropdown from "./ViewDropdown";

/**
 * 
 * The main component for showing search and config options.
 *
 * @returns {object} HTML object - The main page.
 */
export default function MainPage() {
  const {
    setPage,
    view,
    setView,
    views,
    setShow
  } = useContext(AppContext);

  // Getting all the views and changing when clicked in dropdown.
  const viewList = []
  for (let i = 0; i < views.length; ++i) {
    viewList.push(<a onClick={() => setView(views[i])}>{view}</a>);
  }

  return (
    <div>
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
      </head>
      <body>
        <div class="container">
          <br/><br/><br/>
          <div class="jumbotron">
            <ViewModal />
            <h1>🔎MemoSearch</h1>
            <h3>Current View: <Badge bg="secondary">{view}</Badge></h3>
            <Button variant="primary" onClick={() => setShow(true)}>Add View</Button>
            &nbsp;&nbsp;
            <ViewDropdown />
          </div>
          <br />
          <div class="d-flex justify-content-around">
                <div>
                  <img src={link_image} alt=""/>
                  <br />
                  <button class="btn btn-info" onClick={() => setPage("links")}>Links</button>
                </div>
                <div>
                  <img src={screenshot_image} alt=""/>
                  <br />
                  <button class="btn btn-info" onClick={() => setPage("screenshots")}>Screenshots</button>
                </div>
                <div>
                  <img src={notes_image} alt=""/>
                  <br />
                  <button class="btn btn-info" onClick={() => setPage("notes")}>Notes</button>
                </div>
          </div>
          <br /><br />
          <div>
            <div style={{ "text-align": "center" }}>
              <h4>Search</h4>
            </div>
            <SearchBar />
            <br /><br />
            <SearchResults />
          </div>
        </div>
      </body>
    </div>
  )
}
