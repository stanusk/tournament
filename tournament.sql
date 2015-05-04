-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
    id serial,
    name text,
    PRIMARY KEY(id)
);

CREATE TABLE matches (
    player_id integer,
    wins integer,
    matches integer
);