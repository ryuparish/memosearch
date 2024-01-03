-- Links test initial data
INSERT INTO links (id, link, about, date, site_name, related_activity, view)
VALUES
  (0, "https://www.google.com/", "google bro1", "2024-01-02T02:46:36.013Z", "google.com", "searching1", "random view1"),
  (1, "https://www.google.com/", "google bro2", "2024-01-01T02:46:36.013Z", "google.com", "searching2", "all"),
  (2, "https://www.google.com/", "google bro3", "2023-11-12T02:46:36.013Z", "google.com", "searching3", "random view2");

-- Notes test initial data
INSERT INTO notes (id, title, about, date, related_activity, view)
VALUES
  (3, "random note1", "note bro1", "2024-03-02T02:46:36.013Z", "writing note1", "all"),
  (4, "random note2", "note bro2", "2024-02-01T02:46:36.013Z", "writing note2", "random view1"),
  (5, "random note3", "note bro3", "2023-11-12T02:46:36.013Z", "writing note3", "all");

-- Screenshots test initial data
INSERT INTO screenshots (id, caption, about, date, text_in_image, path, related_activity, view)
VALUES
  (6, "screenshot1", "screenshot bro1", "2024-05-02T02:46:36.013Z", "screenshot text1", "random path1", "random related activity1", "random view2"),
  (7, "screenshot2", "screenshot bro2", "2024-06-01T02:46:36.013Z", "screenshot text2", "random path2", "random related activity2","random view2"),
  (8, "screenshot3", "screenshot bro3", "2023-12-12T02:46:36.013Z", "screenshot text3", "random path3", "random related activity3","random view3");
