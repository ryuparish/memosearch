import React, { useState, useContext } from 'react';
import { AppContext } from "../App";
import Button from "react-bootstrap/Button";

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

  /**
   * Handling the submission of screenshots to the server.
   *
   * @param {object} event - the event that triggered the screenshot submission
   */
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
    formData.append("view", view)
    formData.append("date", date)


    // Post to the "links" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/screenshots", {
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
    setPage("main");
  }

  /**
   * Handler for clear calls.
   *
   */
  function handleClear() {
    setScreenshotActivity("");
    setScreenshotCaption("");
    setScreenshotText("");
    setScreenshotFile(null);
    setScreenshotAbout("")
  }

  // Create an img or display N/A if none uploaded
  let imageDisplay = <text>N/A</text>;
  if (screenshotFile) {
    imageDisplay = <img src={URL.createObjectURL(screenshotFile)} alt=""/>;
  }

  return (
    <div>
      <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
        <script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>
      </head>

      <body>
        <br />
        <div class="container">
          <br /><br />
          <button class="btn btn-info" onClick={() => setPage("main")}>Back</button>
          <br /><br />
          <div class="jumbotron">
            <h1>Screenshot</h1>
            <h2>Create a new Screenshot</h2>
          </div>
          <br />
          <form id="links" onSubmit={handleSubmit}>
            <h3> New Screenshot </h3>
            <label for="file">File or Photo Directory:</label>
            <input type="file" name="image" onChange={(e) => { setScreenshotFile(e.target.files[0]) }} /><br />
            {imageDisplay}<br /><br />
            <label for="Caption">Caption:</label>
            <input type="text" id="caption" name="caption" onChange={(e) => setScreenshotCaption(e.target.value)} value={screenshotCaption} /><br /><br />
            <label for="text_in_image">Text in image (if any):</label>
            <input type="text" id="text_in_image" name="text_in_image" onChange={(e) => setScreenshotText(e.target.value)} value={screenshotText} /><br /><br />
            <label for="activity">Related Activity:</label>
            <input type="text" id="activity" name="activity" onChange={(e) => setScreenshotActivity(e.target.value)} value={screenshotActivity} /><br /><br />
            <label for="date">Date:</label>
            <p>{formattedDate}</p><br />
            <label for="about">About:</label><br />
            <textarea id="about" name="freeform" rows="20" cols="100" onChange={(e) => setScreenshotAbout(e.target.value)} value={screenshotAbout}></textarea><br /><br />
            <Button type="submit" class="btn btn-info">Submit</Button>
            &nbsp;&nbsp;
            <Button class="btn btn-info" onClick={handleClear}>Clear</Button>
          </form>
          <p><font color="red"> {screenshotError} </font></p>
        </div>
      </body>
    </div>)
}
