CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS action_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO notes (title, content) VALUES
  ('Welcome', 'This is a starter note. TODO: explore the app!'),
  ('Demo', 'Click around and add a note. Ship feature!');

INSERT INTO action_items (description, completed) VALUES
  ('Try pre-commit', 0),
  ('Run tests', 0);
