DROP TABLE IF EXISTS links_temp;
CREATE TABLE links_temp (id INTEGER PRIMARY KEY, link TEXT NOT NULL, about TEXT NOT NULL, date TEXT NOT NULL, site_name TEXT NOT NULL, related_activity TEXT NOT NULL, view TEXT NOT NULL, description_string TEXT NOT NULL);
INSERT INTO notes_temp (id, link, about, date, site_name, related_activity, view, description_string) SELECT id, link, about, date, site_name, related_activity, view, SUBSTR(about,0,150) || ' ' || related_activity || ' ' || view FROM links;
DROP TABLE links;
ALTER TABLE links_temp RENAME TO links;