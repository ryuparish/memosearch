import React, { useEffect } from "react";
import './App.css';
import MainPage from "./components/MainPage";
import LinksPage from "./components/LinksPage";
import ScreenshotsPage from "./components/ScreenshotsPage";
import NotesPage from "./components/NotesPage";
import SearchResult from "./components/SearchResult";
import NoteEditor from "./components/NoteEditor";
import ScreenshotEditor from "./components/ScreenshotEditor";
import LinkEditor from "./components/LinkEditor";
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";

export const AppContext = React.createContext();

/**
 * Main Application component that returns the Application
 * current page.
 *
 * @returns {object} HTML for a page - This represents the current page
 */
export default function App() {

  // Main Page state
  const [page, setPage] = React.useState("main");
  const [views, setViews] = React.useState(["all"]);
  const [view, setView] = React.useState("all");
  const [show, setShow] = React.useState(false);

  // Google Calendar State
  const [user, setUser] = React.useState(null);
  const [profile, setProfile] = React.useState(null);
  const [calendarEvents, setCalendarEvents] = React.useState({});

  // Link Page state
  const [links, setLinks] = React.useState([]);
  const [linkError, setLinkError] = React.useState("");
  const [htmlFile, setHtmlFile] = React.useState(null)

  // Screenshots Page state
  const [screenshotActivity, setScreenshotActivity] = React.useState("");
  const [screenshotCaption, setScreenshotCaption] = React.useState("");
  const [screenshotText, setScreenshotText] = React.useState("");
  const [screenshotFile, setScreenshotFile] = React.useState();
  const [screenshotAbout, setScreenshotAbout] = React.useState("");
  const [screenshotError, setScreenshotError] = React.useState("");

  // Notes Page state
  const [noteActivity, setNoteActivity] = React.useState("");
  const [noteAbout, setNoteAbout] = React.useState("");
  const [noteTitle, setNoteTitle] = React.useState("");
  const [noteError, setNoteError] = React.useState("");

  // Search Page State
  const [searchQuery, setSearchQuery] = React.useState("");
  const [searchResults, setSearchResults] = React.useState([]);
  const [searchNote, setSearchNote] = React.useState(true);
  const [searchScreenshot, setSearchScreenshot] = React.useState(true);
  const [searchLink, setSearchLink] = React.useState(true);

  // Accumulated State
  const all_states = {
    page,
    setPage,
    linkError,
    setLinkError,
    screenshotActivity,
    setScreenshotActivity,
    screenshotCaption,
    setScreenshotCaption,
    screenshotText,
    setScreenshotText,
    screenshotAbout,
    setScreenshotAbout,
    screenshotFile,
    setScreenshotFile,
    noteActivity,
    setNoteActivity,
    noteAbout,
    setNoteAbout,
    noteTitle,
    setNoteTitle,
    noteError,
    setNoteError,
    searchResults,
    setSearchResults,
    searchQuery,
    setSearchQuery,
    searchNote,
    setSearchNote,
    searchLink,
    setSearchLink,
    searchScreenshot,
    setSearchScreenshot,
    screenshotError,
    setScreenshotError,
    links,
    setLinks,
    htmlFile,
    setHtmlFile,
    view,
    setView,
    views,
    setViews,
    show,
    setShow,
    user,
    setUser,
    profile,
    setProfile,
    calendarEvents,
    setCalendarEvents,
  }

  // Load the Google Calendar 
  // Load the list of possible views initially
  // and load the top five content items from
  // each content group (Note, Screenshot, Link).
  useEffect(() => {
    if (user) {
      fetch("https://www.googleapis.com/calendar/v3/calendars/ryuparish1115@gmail.com/events?key=AIzaSyAdqZjAT9-3uUSIjl8rsZbx4QjNOVCd3wE", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${user.access_token}`
        }
      }).then((response) => {
        return response.json();
      }).then((data) => {
        const events = data.items.filter((e) => {
          // Two week threshold
          const notTooEarly = (new Date(e.created)) >= (Date.now() - 12096e5)
          const notTooLate = (new Date(e.created)) <= (Date.now() + 12096e5)
          return notTooEarly && notTooLate;
        });

        var newCalendarEvents = {...calendarEvents};
        for (var i = 0; i < events.length; i++){
          if (!calendarEvents[events[i].created]){
            newCalendarEvents[events[i].created] = {
              id: events[i].created,
              title: events[i].summary || "something",
              start: events[i].start.dateTime,
              end: events[i].end.dateTime
            }
          }
          setCalendarEvents(newCalendarEvents);
        }

        // Set the events in the calendar if not added yet.
        console.log(events);
        console.log(calendarEvents);
      });
    }

    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/views", {
      credentials: "include",
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let init_views = [];
        for (let i = 0; i < data.length; i++) {
          init_views.push(data[i]);
        }
        setViews(init_views);
      })
      .catch((error) => console.log(error));

    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/topfive", {
      method: "GET",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here are the top fives we received: " + JSON.stringify(data));
        // Collect the search results to put into searchResults
        let top_fives = []
        for (const key in data) {
          let display_field;
          let route;
          switch (key) {
            case "links":
              display_field = "link";
              route = "link";
              break;
            case "screenshots":
              display_field = "caption";
              route = "screenshot";
              break;
            case "notes":
              display_field = "title";
              route = "note";
              break;
            default:
              display_field = "link";
              route = "link";

          }

          // Looping through the ENUMERATION generated by the list in this for-loop
          for (let obj in data[key]) {
            const item_id = data[key][obj]["id"];

            // Use absoute path only in env file for data folder.
            const href = process.env.REACT_APP_FRONTEND_ENDPOINT + "/" + route + "/" + item_id;
            top_fives.push(<SearchResult
              route={route}
              href={href}
              display_field={data[key][obj][display_field]}
              about={data[key][obj]["about"].substring(0, 25)}
            />
            )
          }
          setSearchResults([...top_fives]);
        }
      })
      .catch((error) => console.log(error));
  }, [user])

  // Page changing logic
  if (page === "main") {
    return (
      <Router>
        <Routes>
          <Route index element={<AppContext.Provider value={all_states}>
                                  <GoogleOAuthProvider clientId={"244785002873-4j6tlhji2o8kp1f29ub346ah442qpoi1.apps.googleusercontent.com"}>
                                    <MainPage />
                                  </GoogleOAuthProvider>
                                </AppContext.Provider>} />
          <Route path="/note/:Id" element={<AppContext.Provider value={all_states}><NoteEditor /></AppContext.Provider>} />
          <Route path="/link/:Id" element={<AppContext.Provider value={all_states}><LinkEditor /></AppContext.Provider>} />
          <Route path="/screenshot/:Id" element={<AppContext.Provider value={all_states}><ScreenshotEditor /></AppContext.Provider>} />
        </Routes>
      </Router>
    );
  }
  else if (page === "links") {
    return (
      <AppContext.Provider value={all_states}>
        <LinksPage />
      </AppContext.Provider>
    );
  }
  else if (page === "notes") {
    return (
      <AppContext.Provider value={all_states}>
        <NotesPage />
      </AppContext.Provider>
    );
  }
  else if (page === "screenshots") {
    return (
      <AppContext.Provider value={all_states}>
        <ScreenshotsPage />
      </AppContext.Provider>
    );
  }
}
