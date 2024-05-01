import React, { useRef, useCallback, useContext } from 'react';
import link_image from "../images/link.jpg";
import screenshot_image from "../images/screenshot.jpg";
import notes_image from "../images/notes.png";
import { AppContext } from "../App";
import SearchBar from "./SearchBar";
import SearchResults from "./SearchResults";
import "./style.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import ViewModal from "./ViewModal";
import Badge from 'react-bootstrap/Badge';
import Button from 'react-bootstrap/Button';
import ViewDropdown from "./ViewDropdown";
import Calendar from '@toast-ui/react-calendar';
import '@toast-ui/calendar/dist/toastui-calendar.min.css';
import { useGoogleLogin } from '@react-oauth/google';

/**
 * 
 * The main component's content for showing search and config options.
 *
 * @returns {object} HTML object - The main page content.
 */
export default function MainPageContent() {
  const {
    setPage,
    view,
    setShow,
    setUser,
    calendarEvents
  } = useContext(AppContext); // Getting all the views and changing when clicked in dropdown.

  const login = useGoogleLogin({
    onSuccess: (codeResponse) => setUser(codeResponse),
    onError: (error) => console.log('Login Failed:', error),
  });

  const onAfterRenderEvent = (event) => {
    console.log(event.title);
  };

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
                  <button class="btn btn-info" onClick={() => setPage("links")}>New Link</button>
                </div>
                <div>
                  <img src={screenshot_image} alt=""/>
                  <br />
                  <button class="btn btn-info" onClick={() => setPage("screenshots")}>New Photo</button>
                </div>
                <div>
                  <img src={notes_image} alt=""/>
                  <br />
                  <button class="btn btn-info" onClick={() => setPage("notes")}>New Note</button>
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
          <div>
            <Calendar 
              height="900px"
              view="week"
              events={Object.values(calendarEvents)}
              month={{
                visibleWeeksCount: 2,
              }}
              useFormPopup={true}
              useDetailPopup={true}
              onAfterRenderEvent={onAfterRenderEvent}
            />
            <button class="btn btn-info" onClick={() => login()}>Google Sign In</button>
            <br/>
            <br/>
          </div>
        </div>
      </body>
    </div>
  )
}
