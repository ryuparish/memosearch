import React, { useContext } from 'react';
import link_image from "../images/link.jpg";
import screenshot_image from "../images/screenshot.jpg";
import notes_image from "../images/notes.png";
import {AppContext} from "../App";
import SearchBar from "./SearchBar";
import SearchResults from "./SearchResults";
import "./style.css";

export default function MainPage() {
  const {setPage} = useContext(AppContext);

  return (
       <div>
         <head>
           <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
           <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>
         </head>
         <body>
           <div class="container">
             <div class="jumbotron">
               <h1>Memosearch</h1>
               <p>Search for links and screenshots</p>
             </div>
             <br/>
           <div class="row">
             <div class="column" style={{"text-align":"center"}}>
               <img style={{"width":"30%"}}src={link_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("links")}>Links</button>
             </div>
             <div class="column" style={{"text-align":"center"}}>
               <img style={{"width":"30%"}} src={screenshot_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("screenshots")}>Screenshots</button>
             </div>
             <div class="column" style={{"text-align":"center"}}>
               <img style={{"width":"30%"}} src={notes_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("notes")}>Notes</button>
             </div>
           </div>
           <br/><br/>
           <div>
             <div style={{"text-align":"center"}}>
               <h4>Search</h4>
             </div>
             <SearchBar/>
           <br/><br/>
             <SearchResults/>
           </div>
         </div>
         </body>
       </div>
    )
}
