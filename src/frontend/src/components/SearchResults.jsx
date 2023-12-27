import React, { useContext } from 'react';
import { AppContext } from "../App";

/**
 * Component for displaying search results state.
 *
 * @returns {object} html object - This represents the search results in HTML.
 */
export default function SearchResults() {
  const {
    searchResults,
  } = useContext(AppContext);


  let searchResult = <text>No Results</text>;
  if (Object.keys(searchResults).length !== 0) {
    searchResult = <ul>{searchResults}</ul>;
  }

  return (
    <div>
      <div class="container">
        <h4><a>Results:</a></h4>
        <div class="slider" >
          {searchResult}
        </div>
      </div>
      <br /><br /><br />
    </div>
  )
}
