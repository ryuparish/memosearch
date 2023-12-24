import React, { useContext } from 'react';
import {AppContext} from "../App";

export default function SearchResults() {
  const {
    searchResults,
  } = useContext(AppContext);

  return (
    <div>
      <div class="container">
        <h4><a>Results:</a></h4>
        <div class="slider" >
          <ul>
            {searchResults}
          </ul>
        </div>
      </div>
    </div>
  )}
