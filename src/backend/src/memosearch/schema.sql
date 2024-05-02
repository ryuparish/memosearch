CREATE TABLE links (
  id INTEGER PRIMARY KEY,
  link TEXT NOT NULL,
  about TEXT NOT NULL,
  date TEXT NOT NULL,
  site_name TEXT NOT NULL,
  related_activity TEXT NOT NULL,
  view TEXT NOT NULL,
  description_string TEXT NOT NULL
);

CREATE TABLE screenshots (
  id INTEGER PRIMARY KEY,
  caption TEXT NOT NULL,
  about TEXT NOT NULL,
  date TEXT NOT NULL,
  text_in_image TEXT NOT NULL,
  path TEXT NOT NULL,
  related_activity TEXT NOT NULL,
  view TEXT NOT NULL,
  description_string TEXT NOT NULL
);

CREATE TABLE notes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  about TEXT NOT NULL,
  date TEXT NOT NULL,
  related_activity TEXT NOT NULL,
  view TEXT NOT NULL,
  description_string TEXT NOT NULL
);
