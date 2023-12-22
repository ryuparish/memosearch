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
  if (page === "main") {
    return (
      <AppContext.Provider value={[page, setPage]}>
        <MainPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "links"){ 
    return (
      <AppContext.Provider value={[page, setPage]}>
        <LinksPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "notes"){ 
    return (
      <AppContext.Provider value={[page, setPage]}>
        <NotesPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "screenshots"){ 
    return (
      <AppContext.Provider value={[page, setPage]}>
        <ScreenshotsPage/>
      </AppContext.Provider>
    );
  }
  else if (page === "Search"){ 
    return (
      <AppContext.Provider value={[page, setPage]}>
        <SearchPage/>
      </AppContext.Provider>
    );
  }
}
