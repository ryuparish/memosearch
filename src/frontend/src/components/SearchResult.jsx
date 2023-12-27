import React, { useContext } from 'react';
import { AppContext } from "../App";

/**
 * A search bar component for searching api database.
 *
 * @param {string} props - props of the route
 * @returns {object} HTML object - HTML representing the search bar
 */
export default function SearchResult(props) {
  let content_type;
  let color;
  switch(props.route){
    case "link":
      content_type = "link";
      color = "DarkOrange";
      break;
    case "screenshot":
      content_type = "image";
      color = "Black";
      break;
    case "note":
      content_type = "description";
      color = "Beige";
      break;
    default:
      content_type = "link";
      color = "DarkOrange";
  }
  return (
    <li>
      <i style={{ "color": color }} class="material-icons">{content_type}</i><a href={props.href} target="_blank">{props.display_field}</a>&nbsp;({props.about}...)
    </li>
  )
}
