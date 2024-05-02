import React, { useContext } from 'react';
import { AppContext } from "../App";

/**
 * A component for configuring links
 *
 * @returns {object} HTML object - The link table component
 */
export default function LinkTable() {
  const {
    linkError,
    setLinkError,
    links,
    setLinks,
    htmlFile,
    setHtmlFile,
    view
  } = useContext(AppContext);

  const date = new Date();

  /**
   * Function for loading links file into links state.
   *
   */
  function handleLinks() {
    // Parse HTML file
    if (htmlFile) {
      const newReader = new FileReader();
      newReader.onload = (() => {
        return function(e) {
          // The first five anchors from Firefox are for automatically generated bookmarks
          const parser = new DOMParser();
          const htmlDoc = parser.parseFromString(e.target.result, "text/html");
          const anchors = htmlDoc.getElementsByTagName("a");
          let newLinks = [];
          for (let i = 5; i < anchors.length; i++) {
            // Finding http://<something> from link and using
            // site_name if match found.
            let matches = anchors[i].href.match(/^https?\:\/\/([^/?#]+)(?:[/?#]|$)/i);
            let domain = matches && matches[1];
            newLinks.push({
              id: Math.floor(Math.random() * 65536),
              about: "",
              link: anchors[i].href,
              date: date,
              site_name: domain ? matches[1] : "",
              related_activity: "",
              status: "New",
              view: view
            });
          }
          setLinks(links.concat(newLinks));
        }
      })(htmlFile);
      newReader.readAsText(htmlFile);
    }
    return;
  }

  /**
   * Handles the link change for each row of table
   *
   * @param {object} event - [TODO:description]
   * @param {[TODO:type]} id - [TODO:description]
   * @returns {[TODO:type]} [TODO:description]
   */
  function handleLinkChange(event, id) {
    setLinks(links.map(link => {
      if (link.id !== id) {
        // No change
        return link;
      } else {
        var matches = event.target.value.match(/^https?\:\/\/([^/?#]+)(?:[/?#]|$)/i);
        var domain = matches && matches[1];
        var newSiteName = link.site_name;
        // Set domain (site_name) only if there is a valid link
        if (domain) {
          newSiteName = matches[1]
        }        // Return a new link
        return {
          id: link.id,
          about: link.about,
          link: event.target.value,
          date: date,
          site_name: newSiteName,
          related_activity: link.related_activity,
          status: "New",
          view: view,
        };
      }
    }));
  }

  function handleAboutChange(event, id) {
    setLinks(links.map(link => {
      if (link.id !== id) {
        // No change
        return link;
      } else {
        // Return a new link
        return {
          id: link.id,
          about: event.target.value,
          link: link.link,
          date: date,
          site_name: link.site_name,
          related_activity: link.related_activity,
          status: "New",
          view: link.view
        };
      }
    }));
  }

  function handleActivityChange(event, id) {
    setLinks(links.map(link => {
      if (link.id !== id) {
        // No change
        return link;
      } else {
        // Return a new link
        return {
          id: link.id,
          about: link.about,
          link: link.link,
          date: date,
          site_name: link.site_name,
          related_activity: event.target.value,
          status: "New",
          view: link.view
        };
      }
    }));
  }

  function handleAddButton() {
    // Following the link structure in the scheme models
    setLinks([...links,
      {
        id: Math.floor(Math.random() * 65536),
        link: "",
        about: "",
        date: date,
        site_name: "",
        related_activity: "",
        status: "New",
        view: view
      }
    ])
  }

  // Get the submitted values and call the python backend
  // to create the database entry
  function handleSubmit(event) {
    event.preventDefault()

    // WHAT DO WE DO ABOUT MULTIPLE FILE UPLOADS?
    // THis is links so we dont have to worry yet, but we should figure it out.

    // Only allow database insertion on a link that has valid 
    // inputs
    setLinkError("")

    // Loop over the links in links state and send lists of JSONs to flask.
    links.forEach((link) => {
      if (link.site_name === "") {
        setLinkError("The site of the links is required")
      } else if (link.link === "") {
        setLinkError("The links are required")
      } else if (link.related_activity === "") {
        setLinkError("The activity of the links is required")
      } else if (link.about === "") {
        setLinkError("The about of the links is required")
      }

    })

    if (linkError !== "") {
      return;
    }

    // Post to the "links" api
    fetch(process.env.REACT_APP_BACKEND_ENDPOINT + "/links", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(links) // Modify this links to have an additional JSON field desc_string
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Here is the data we put into the database: " + JSON.stringify(data));
        setLinks(links.map(link => {
          return {
            id: link.id,
            about: link.about,
            link: link.link,
            date: date,
            site_name: link.site_name,
            related_activity: link.related_activity,
            status: "Done",
            view: link.view
          };
        }));
      })
      .catch((error) => console.log(error));
  }

  // Generating the link items to show in the link table.
  let link_items = [];
  for (const link_num in links) {
    const link_item = links[link_num];
    link_items.push(
      <tr>
        <td><input value={link_item["site_name"]} onChange={() => { }} ></input></td>
        <td><input value={link_item["link"]} onChange={(e) => handleLinkChange(e, link_item["id"])} ></input></td>
        <td><input value={link_item["related_activity"]} onChange={(e) => handleActivityChange(e, link_item["id"])} ></input></td>
        <td><input value={link_item["about"]} onChange={(e) => handleAboutChange(e, link_item["id"])} ></input></td>
        <td><input value={link_item["view"]} onChange={() => { }} ></input></td>
        <td><span class="status text-success">•</span>{link_item["status"]}</td>
        <td>
          <a onClick={() => { setLinks(links.filter(a => a.id !== link_item["id"])) }} href="#"><i value="1" class="editItem material-icons" style={{ "cursor": "pointer" }}>remove</i></a>
        </td>
      </tr>
    );
  }

  return (
    <form id="link" onSubmit={handleSubmit}>
      <div class="container">
        <div class="table-wrapper">
          <div class="table-title">
            <div class="row">
              <div class="col-sm-4">
                <h2>New <b>Links</b></h2>
              </div>
              <div class="col-sm-8">
                <a href="#" class="btn btn-info"><i class="material-icons">file_download_done</i><input value={"Submit Links"} type="submit" /></a>
              </div>
            </div>
          </div>
          <table class="table table-striped table-hover">
            <thead>
              <tr>
                <th>Site</th>
                <th>Link</th>
                <th>Activity</th>
                <th>About</th>
                <th>View</th>
                <th>Status</th>
                <th>Remove</th>
              </tr>
            </thead>
            <tbody id="tbody">
              {link_items}
            </tbody>
          </table>
          <div class="clearfix">
            <ul id="pagination" class="pagination">
              <li class="page-item disabled"><a onClick={() => setLinks([])}>Clear</a></li>
              <li class="page-item"><a onClick={handleAddButton} class="page-link">Add Link</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="row col-sm-4 container">
        <input onChange={(e) => setHtmlFile(e.target.files[0])} type="file" />
        <a onClick={handleLinks} class=""><input value="Upload Links" type="submit" /></a>
      </div>
      <br/><br/><br/><br/>
    </form>
  )
}
