import React, { useContext } from 'react';
import {AppContext} from "../App";
import SearchBar from "./SearchBar";
import SearchResults from "./SearchResults";

export default function SearchPage() {
  const {
    setPage,
    searchQuery,
    setSearchQuery,
    searchResults,
    setSearchResults,
    searchNote,
    setSearchNote,
    searchScreenshot,
    setSearchScreenshot,
    searchLink,
    setSearchLink,
  } = useContext(AppContext);

  let result_list = [];

  // Handle when the search button is clicked
  function handleSearch(event) {
    event.preventDefault()
    let content =  []
    
    // Adding content types
    if (searchNote) {
      content.push("notes")
    }
    if (searchScreenshot) {
      content.push("screenshots")
    }
    if (searchLink) {
      content.push("links")
    }

    console.log("Here is the searchQuery: " + searchQuery);
    fetch("http://127.0.0.1:4444/search", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({"search": searchQuery, "content": content})
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // Logic for finding the type then displaying correctly in link list
        for (const key in data) {
          let display_field;
          switch (key){
            case "links":
              display_field = "link";
              break;
            case "screenshots":
              display_field = "caption";
              break;
            case "notes":
              display_field = "title";
              break;
            default:
              display_field = "link";

          }
              
          // Looping through the ENUMERATION generated by the list in this for-loop
          for (let obj in data[key]) {
            console.log(data[key][obj]);
            result_list.push(<li><text>{'[' + key.toUpperCase() +'] '}</text><a>{data[key][obj][display_field]}</a></li>)
          }
        }
        setSearchResults(result_list);
      })
        .catch((error) => console.log(error));
  }
  
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
            <h1>Search</h1>
            <h2>Search for links, screenshots, and notes.</h2>
          </div>
          <SearchBar/>
          <SearchResults/>
        </div>
      </body>
    </div>
  )}