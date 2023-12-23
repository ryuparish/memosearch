import React, { useState, useContext } from 'react';
import {AppContext} from "../App";
// Use fetch() instead.
//import axios from 'axios';


// Send multiple files to a server.
// Example of processing many files by sending to a server.
// We want to do this with our flask backend server.
//export const function App() {
//
//  const [file, setFile] = useState()
//
//  function handleChange(event) {
//    setFile(event.target.files[0])
//  }
//  
//  function handleSubmit(event) {
//    event.preventDefault()
//    const url = 'http://localhost:3000/uploadFile';
//    const formData = new FormData();
//    formData.append('file', file);
//    formData.append('fileName', file.name);
//    const config = {
//      headers: {
//        'content-type': 'multipart/form-data',
//      },
//    };
//    axios.post(url, formData, config).then((response) => {
//      console.log(response.data);
//    });
//
//  }
//
//  return (
//    <div className="App">
//        <form onSubmit={handleSubmit}>
//          <h1>React File Upload</h1>
//          <input type="file" onChange={handleChange}/>
//          <button type="submit">Upload</button>
//        </form>
//    </div>
//  );
//}

export default function ScreenshotsPage() {
  const {
    setPage,
    screenshotActivity,
    setScreenshotActivity,
    screenshotCaption,
    setScreenshotCaption,
    screenshotText,
    setScreenshotText,
    screenshotFile,
    setScreenshotFile,
    screenshotAbout,
    setScreenshotAbout
  } = useContext(AppContext);
  const date = new Date();
  const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
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
          <h1>Configure Screenshots</h1>
          <h2>Add, Delete, and Edit Screenshot data</h2>
        </div>
        <br/>
        <form id="links">
          <h3> Add Screenshot </h3>
            <label for="file">File or Photo Directory:</label>
          <input type="file" onChange={(e) => setScreenshotFile(e.target.value)} value={screenshotFile}/><br/>
            <label for="Caption">Caption:</label>
          <input type="text" id="caption" name="caption" onChange={(e) => setScreenshotCaption(e.target.value)} value={screenshotCaption}/><br/><br/>
            <label for="text_in_image">Text in image (if any):</label>
              <input type="text" id="text_in_image" name="text_in_image" onChange={(e) => setScreenshotText(e.target.value)} value={screenshotText}/><br/><br/>
            <label for="activity">Related Activity:</label>
              <input type="text" id="activity" name="activity" onChange={(e) => setScreenshotActivity(e.target.value)} value={screenshotActivity}/><br/><br/>
            <label for="date">Date:</label>
              <p>{formattedDate}</p><br/>
            <label for="about">About:</label><br/>
              <textarea id="about" name="freeform" rows="4" cols="50" onChange={(e) => setScreenshotAbout(e.target.value)} value={screenshotAbout}></textarea><br/><br/>
          <button type="submit" class="btn btn-info" onClick={() => {}}>Submit</button>
        </form>
      </div>
    </body>
  </div>)
}
