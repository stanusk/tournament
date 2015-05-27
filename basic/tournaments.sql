-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE tournaments;
CREATE DATABASE tournaments;
\c tournaments

-- Tables --
CREATE TABLE players (
    id serial PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE matches (
    player_id integer REFERENCES players(id) ON DELETE CASCADE,
    wins integer NOT NULL,
    matches integer NOT NULL
);

-- Views --
CREATE VIEW v_newPlayerID AS
    SELECT id FROM players ORDER BY id DESC LIMIT 1;

CREATE VIEW v_standings AS
    SELECT players.id, players.name, matches.wins, matches.matches
    FROM players, matches WHERE players.id = matches.player_id ORDER BY matches.wins
    DESC, matches.matches DESC;