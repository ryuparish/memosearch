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
    calendarEvents,
    user,
    newEventName,
    setNewEventName,
    newEventType,
    setNewEventType
  } = useContext(AppContext); // Getting all the views and changing when clicked in dropdown.

  // Login to Google to see Calendar
  const login = useGoogleLogin({
    scope: [
      "openid",
      "https://www.googleapis.com/auth/userinfo.profile",
      "https://www.googleapis.com/auth/userinfo.email",
      "https://www.googleapis.com/auth/calendar.readonly",
      "https://www.googleapis.com/auth/calendar.events",
    ].join(" "),
    onSuccess: (codeResponse) => setUser(codeResponse),
    onError: (error) => console.log('Login Failed:', error),
  });

  // Send new event object to google calendar
  function handleEventSubmit(event) {
    event.preventDefault()
    var formData = new FormData(event.target);

    // Post to the google calendar api to create event
    if (user) {
      fetch("https://www.googleapis.com/calendar/v3/calendars/ryuparish1115@gmail.com/events?key=AIzaSyAdqZjAT9-3uUSIjl8rsZbx4QjNOVCd3wE", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${user.access_token}`
        },
        body: JSON.stringify({
          end: {
            "dateTime": new Date(formData.get("endTime")),
            "timeZone": Intl.DateTimeFormat().resolvedOptions().timeZone
          },
          start: {
            "dateTime": new Date(formData.get("startTime")),
            "timeZone": Intl.DateTimeFormat().resolvedOptions().timeZone
          },
          summary: formData.get("eventName"),
        })
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          console.log("Here is the data we put into the database: " + JSON.stringify(data));
        })
        .catch((error) => console.log(error));
    }
  }

  return (
    <div>
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
      </head>
      <body>
        <div class="container">
          <br /><br /><br />
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
              <img src={link_image} alt="" />
              <br />
              <button class="btn btn-info" onClick={() => setPage("links")}>New Link</button>
            </div>
            <div>
              <img src={screenshot_image} alt="" />
              <br />
              <button class="btn btn-info" onClick={() => setPage("screenshots")}>New Photo</button>
            </div>
            <div>
              <img src={notes_image} alt="" />
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
            <fieldset style={{ padding: '0 20px 20px 20px' }}>
              <legend>
                <h2> Add An Event </h2>
              </legend>
              <form name='myForm' onSubmit={handleEventSubmit}>
                <table>
                  <tr>
                    <td>Name:</td>
                    <td><input type="text" name="eventName" onChange={(e) => setNewEventName(e.target.value)} required /></td>
                  </tr>
                  <tr>
                    <td>Start Time:</td>
                    <td><input type="datetime-local" name="startTime" required /></td>
                  </tr>
                  <tr>
                    <td>End Time:</td>
                    <td><input type="datetime-local" name="endTime" required /></td>
                  </tr>
                  <tr>
                    <td><input type="submit" id="addEventBTN" value="Add Event" /></td>
                  </tr>
                </table>
              </form>
            </fieldset>
            <br />
            <Calendar
              height="900px"
              view="week"
              events={Object.values(calendarEvents)}
              month={{
                visibleWeeksCount: 4,
              }}
              useFormPopup={true}
              useDetailPopup={true}
            />
            <button class="btn btn-info" onClick={() => login()}>Google Sign In</button>
            <br />
            <br />
          </div>
        </div>
      </body>
    </div>
  )
}
