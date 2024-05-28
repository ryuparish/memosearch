# Memo Search Notes and Screenshot Search Tool

## Executive Summary:

  A desktop application that searches Notes, screenshots, and bookmarks.

  Stores each item with context for remembering when found later.

  Uses email and Google Calendar to remind, schedule, and show problems.

## Infrastructure Design:
> This project initially followed this setup to get started: https://flask.palletsprojects.com/en/3.0.x/tutorial/ , it was a very important part of this project.

## Frontend 


#### The frontend consists of Electron and React (Javascript) container that communicates to the Memosearch backend (Python)

### 1. Features

+ Pages
    1. Every Page
        1. Separate pop up window for editing fields and or deletion. We will need to use react-router-dom to solve our multiple-window issue.
            - Specifically, we can use content ids and their data for this type of dynamic route: https://reactrouter.com/en/main/route/route#path

        2. Editor for a content items
            - Easy to switch from item to item within the content type

        3. Bulk adding content items

        4. Related items that come with opening items in their editors.

    2. Main Page
        - Buttons to all Links, Notes, and Screenshots configuration
        - Search bar and results
          - Autoload this with the top k most recent additions to the database.
          - Results should show:
            - Content type
            - Preview of the about
            - A Link if found
            - Date of the content

    3. Links page
        - Allow for multiple link uploads.
          - Multi-upload should allow for an interactive frontend.
        - Clear page fields and load success message on sucessful
        submission.
        - Textbox to add a new link
        - Textboxes for each of the following:
          - About
          - Site Name
          - Date
          - Related Activity (predicted activity)
        - Error message that automatically loads to show that validation for the link occurred.
        - Upload button

    4. Images page
        - Allow for multiple Image uploads.
        - Image Upload button
        - Textboxes for each of the following:
          - About
          - Caption
          - Image in text
          - Date
          - Related Activity (predicted activity)
        - Error message that automatically loads to show that validation for the image occurred.
        - Upload button

    5. Notes page
      - Allow for multiple Note uploads.
      - Textbox to add a new note
      - Textboxes for each of the following:
        - About
        - Date
        - Related Activity (predicted activity)
      - Error message that automatically loads to show that validation for the note occurred.
      - Upload Button

+ Email a list of todo items based on their activity.
  - Attach things that are useful.

+ Calendar
    - Allows for creating, deleting, and modifying meetings/events.
    - Currently, we can log in through the google sign in and save session data in the browser.



## Backend

#### The backend consists of a django server that feeds endpoints to the React frontend.
#### The server uses two databases, one for vectors (similarity search) and one for memo objects.
> The documentation for the backend uses Sphinx formatting and can generate documentation using Sphinx.


### 1. Features:
  + A text generation mvc model that:
    - Extracts screenshots to textual descriptions
    - Extracts notes into author's thoughts
    - Extracts bookmarks into TODO activities

  + A classicfication mvc model that:
    - Clusters all the textual data into categories
    - Asks user if they could classify the topic of the text, with one k-mean getting one topic.

  + A database for memos:
    - Each of the operations of the database are the main operations involved in the Memosearch app (Saving and retrieving Images, text, and Links)

  + A database for vectors:
    - Storage / Entry
        - For every new note, image, and link, create a description-string made from the object data and
        vectorize it. Once vectorized, we check to see if the vector has already been entered 
        and if not, we enter it into the database.

    - Retrieval
        - When retrieving, we first transform the description-string into a vector and search 
        for similar vectors and then finally return the corresponding ids to the caller.


3. Testing

  React Testing:
    - Jest

  Flask Testing:
    - pytest

Case Study:

Often times, Ryu is scrolling through the internet whilst tired, travelling, and/or about to do something important. In those moments,
sometimes he sees something that is worth keeping note of, but not acting upon right away. Ryu screenshots the IPhone/Mac screen,
bookmarks the page, and/or makes a note in his IPhone notes app. Eventually, Ryu forgets about these memos and finds them again, completely
confused by what the context was. If he has possibly been reminded of it the next day, he could wrote some context for it and started
something, or perhaps wrote some context and saved it for later date.


  Happy Path: 

    This is where Ryu thought about creating a system that would:
    
      1. Save the screenshot, note, or bookmark.
    
      2. Remind Ryu of screenshots with no context, so that
      he actually understands what they were for in the future.
    
      3. Extract text from screenshots and bookmarked pages to
      allow for search on these memos when he thinks about them
      later on.
    
      4. Do analytics and keep track of what type of content he is saving 
      and suggest some ways to explore his ideas.


Dying Wish:
  
The application is really detailed for each of the three content types and each content type feels completely maxed out.
Then again, the searching makes them feel all the same when searched.

Log:

  27/12/23: Application Complete

  29/12/23: Declarative Flask-SQLAlchemy issues with Application Factories
    
    Error: KeyError: <weakref at 0x7fcb3756a770; to 'Flask' at 0x7fcb34edf640> 

    Cause: Declarative use of SQLAlchemy: top_5_links = Link.query.order_by(Link.date.desc()).limit(5).all()

    - Declarative Flask-SQLAlchemy requires a call to create_engine() in order
    to setup the database connection. This is recommended to do for declarative SQLAlchemy in
    a file called database.py (https://flask.palletsprojects.com/en/3.0.x/patterns/sqlalchemy/).

    However, we cannot do this connection of the database
    during the execution of the application factory (which cannot be global)
    to establish the database connection/file to use by the app when factoried.
    This is because the Declarative SQLAlchemy docs use the db connection as a 
    global variable, not in the factory product context.

  ~ 15/04/24: Added Google Calendar integration to display calendar and events.

  30/04/24: Dealing with Similarity Search

    - There is a little issue. If we want to use this 
    tutorial: https://python.langchain.com/docs/integrations/vectorstores/sqlitevss/ we
    need to have a quick load time for the database since we need to load it everytime in order to 
    use upon a search. Moreover, we need to have some sort of design to the vector database 
    operations.
        - SOLUTION: With a small enough model, load times aren't that long at all.

  31/04/24: Dealing with Sphinx documentation

    - The documentation for Sphinx doesn't work for decorated functions that can't be 
    resolved (such as mock libraries used by decorators). We need to figure out a way 
    to get the libraries non-mocked, or somehow find a way to get past the decorator problem.
        - SOLUTION: Turns out that I was using a python version within the brew-installed Sphinx
        and it did not recognize the conda environments libraries and was looking at sys.path without
        looking at my current conda library.

  05/05/24: Dealing with streamlining adding content

    - The ideal way to get all the content we want to submit is by having
        - A system to get all notes on my IPhone
        - A system to get all the screenshots from my iphone and from my mac 
        - A system to get all the links in my firefox folder
        - Ideally, all in one place.

  23/05/24: Dealing with automatically adding additional context to memos 

    - We need to find ways to automatically added text from images into their metadata, along 
    with:
        - Suggesting what type of goal/activity was being prepared or scheduled.
        - Suggesting what steps need to be taken in order to do that activity.
        - Suggesting what resources would be most helpful in getting that activity done.
        - Grouping things into categories.

  24/05/24: Adding events to google calendar through the webapp.

    - It would be nice if we could add events to the calendar without having to go through the google calendar app, just a simple form to fill out and send
    to google calendar for it to create an event.
        - Use Google Calendar API to send through the Javascript frontend.
