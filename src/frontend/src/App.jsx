import React from "react";
import './App.css';
import MainPage from "./components/MainPage";
import LinksPage from "./components/LinksPage";
import ScreenshotsPage from "./components/ScreenshotsPage";
import NotesPage from "./components/NotesPage";
import SearchPage from "./components/SearchPage";

export const AppContext = React.createContext();
export default function App() {
  const [page, setPage] = React.useState("main");

  // Link Page state
  const [linkName, setLinkName] = React.useState("");
  const [link, setLink] = React.useState("");
  const [linkActivity, setLinkActivity] = React.useState("");
  const [linkAbout, setLinkAbout] = React.useState("");
  const [linkError, setLinkError] = React.useState("");

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
    linkName,
    setLinkName,
    link,
    setLink,
    linkActivity,
    setLinkActivity,
    linkAbout,
    setLinkAbout,
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
    setScreenshotError
  }

  // Page changing logic
  if (page === "main") {
    return (
      <AppContext.Provider value={all_states}>
        <MainPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "links"){ 
    return (
      <AppContext.Provider value={all_states}>
        <LinksPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "notes"){ 
    return (
      <AppContext.Provider value={all_states}>
        <NotesPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "screenshots"){ 
    return (
      <AppContext.Provider value={all_states}>
        <ScreenshotsPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "search"){ 
    return (
      <AppContext.Provider value={all_states}>
        <SearchPage/>
      </AppContext.Provider>
    );
  }
}
