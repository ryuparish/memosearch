import React, { useContext } from 'react';
import link_image from "../images/link.jpg";
import screenshot_image from "../images/screenshot.jpg";
import notes_image from "../images/notes.png";
import search_image from "../images/search.jpg";
import {AppContext} from "../App";

export default function MainPage() {
  const [page, setPage] = useContext(AppContext);

  return (
       <div>
         <head>
           <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"/>
         </head>
         <body>
           <div class="container">
             <div class="jumbotron">
               <h1>Memosearch</h1>
               <p>Search for links and screenshots</p>
             </div>
             <br/>
             <div class="row">
             <div class="col-xs-3">
               <img style={{"width":"30%"}}src={link_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("links")}>Links</button>
             </div>
             <div class="col-xs-3">
               <img style={{"width":"30%"}} src={screenshot_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("screenshots")}>Screenshots</button>
             </div>
             <div class="col-xs-3">
               <img style={{"width":"30%"}} src={notes_image} alt=""/>
               <br/>
               <button class="btn btn-info" onClick={() => setPage("notes")}>Notes</button>
             </div>
             <div class="col-xs-3">
               <img style={{"width":"40%","padding":"5px"}} src={search_image} alt=""/>
               <br/>
               <button class="btn btn-warning" onClick={() => setPage("search")}>Search</button>
             </div>
           </div>
         </div>
         </body>
       </div>
    )
}
