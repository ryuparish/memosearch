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
    setScreenshotAbout,
    screenshotError,
    setScreenshotError,
    view
  } = useContext(AppContext);
  const date = new Date();
  const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;

  function handleSubmit(event) {
    event.preventDefault()

    // Only allow database insertion on a link that has valid 
    // inputs
    setScreenshotError("")
    if (screenshotFile === undefined) {
      setScreenshotError("The file of the screenshot is required")
    } else if (screenshotCaption === "") {
      setScreenshotError("The screenshot caption is required")
    } else if (screenshotText === "") {
      setScreenshotError("The screenshot text is required")
    } else if (screenshotActivity === "") {
      setScreenshotError("The activity of the screenshot is required")
    } else if (screenshotAbout === "") {
      setScreenshotError("The about of the screenshot is required")
    }

    if (screenshotError !== "") {
      console.log("Returning due to empty fields")
      return;
    }

    // Putting the image into a form so flask can read in
    const formData = new FormData()
    formData.append("file", screenshotFile)
    formData.append("caption", screenshotCaption)
    formData.append("text", screenshotText)
    formData.append("activity", screenshotActivity)
    formData.append("about", screenshotAbout)
    formData.append("date", date)

    // Create a new link object and send to the server
    // const screenshotObj = {
    //   file:formData,
    //   caption:screenshotCaption,
    //   activity:screenshotActivity,
    //   about:screenshotAbout,
    //   date:date
    // }

    console.log("Sending this form data: " + formData.get("file"))
    // Post to the "links" api
    fetch("http://127.0.0.1:4444/screenshots", {
      method: "POST",
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
      body: formData
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the data we put into the database: " + JSON.stringify(data[0]));
      })
      .catch((error) => console.log(error));
  }

  console.log("Here is the screenshotFile: " + screenshotFile)
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
        <form id="links" onSubmit={handleSubmit}>
          <h3> Add Screenshot </h3>
            <label for="file">File or Photo Directory:</label>
          <input type="file" name="image" onChange={(e) => {setScreenshotFile(e.target.files[0])}} /><br/>
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
              <input type="submit" id="submit" name="submit"/>
        </form>
        <p><font color="red"> {screenshotError} </font></p>
      </div>
    </body>
  </div>)
}
