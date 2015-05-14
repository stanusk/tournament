/* PostgreSQL database for Swiss style tournament. */


/* Create db */
DROP DATABASE tournaments;
CREATE DATABASE tournaments;
\c tournaments


/* Establish schema */
-- data types --
CREATE TYPE tourStatus AS ENUM ('planned', 'ongoing', 'closed');
CREATE TYPE playerStatus AS ENUM ('active', 'inactive');


-- tables --
CREATE TABLE tournaments (
    id serial PRIMARY KEY,
    name text,
    status tourStatus
);

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text,
    status playerStatus
);


-- views --
CREATE VIEW v_toursCount AS
    SELECT status, count(*)
    FROM tournaments
    GROUP BY status;

CREATE VIEW v_playersCount AS
    SELECT status, count(*)
    FROM players
    GROUP BY status;


/* Populate db */
-- tournaments
INSERT INTO tournaments VALUES (default, 't_tour1', 'planned');
INSERT INTO tournaments VALUES (default, 't_tour2', 'ongoing');
INSERT INTO tournaments VALUES (default, 't_tour3', 'ongoing');
INSERT INTO tournaments VALUES (default, 't_tour4', 'closed');
INSERT INTO tournaments VALUES (default, 't_tour5', 'closed');
INSERT INTO tournaments VALUES (default, 't_tour6', 'closed');

-- players
INSERT INTO players VALUES (default, 't_player1', 'active');
INSERT INTO players VALUES (default, 't_player2', 'active');
INSERT INTO players VALUES (default, 't_player3', 'inactive');
INSERT INTO players VALUES (default, 't_player4', 'inactive');
INSERT INTO players VALUES (default, 't_player5', 'inactive');