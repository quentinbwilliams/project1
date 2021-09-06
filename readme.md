# Matchday

Follow your favorite football leagues and clubs with the Matchday app, featuring live standings, scores, upcoming matches, player stats, injury and transfer news. Sign in to support your favorite club, follow players, and chat with others during live matches.

## Design

Matchday is built with Flask and will utilize React for the front-end.
API Football is called on the server-side, which populates a Postgres database at set intervals.
Client-side logic queries the database in most cases.
