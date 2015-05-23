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
    name text NOT NULL,
    status tourStatus NOT NULL
);

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text NOT NULL,
    status playerStatus NOT NULL
);

CREATE TABLE registrations (
    id serial PRIMARY KEY,
    -- ON DELETE CASCADE is set to simplify testing since deleting is
    -- restricted to admins (for testing only)
    tour_id int NOT NULL REFERENCES tournaments (id) ON DELETE CASCADE,
    player_id int NOT NULL REFERENCES players (id) ON DELETE CASCADE,
    UNIQUE (tour_id, player_id)
);

CREATE TABLE matchesRaw (
    id serial PRIMARY KEY,
    -- ON DELETE CASCADE is set to simplify testing since deleting is
    -- restricted to admins (for testing only)
    tour_id int NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    pl1_id int NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    pl1_score int NOT NULL,
    pl2_id int NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    pl2_score int NOT NULL
);


-- views --

-- tournaments:
CREATE VIEW v_toursCountByStatus AS
    SELECT status, count(*)
    FROM tournaments
    GROUP BY status;

-- players:
CREATE VIEW v_playersCountByStatus AS
    SELECT status, count(*)
    FROM players
    GROUP BY status;

-- matches:
CREATE VIEW v_matchWinners AS
    SELECT id,
           -- select id of player with higher score as winner or leave empty
           -- (null) in case of a draw
           CASE WHEN pl1_score > pl2_score THEN pl1_id
                WHEN pl1_score < pl2_score THEN pl2_id
           END as winner_id
    FROM matchesRaw;

CREATE VIEW v_matches AS
    SELECT r.*, w.winner_id
    FROM matchesRaw AS r JOIN v_matchWinners as w ON r.id = w.id;


/* Populate db */

-- tournaments
INSERT INTO tournaments VALUES (default, 't_tour1', 'planned');
INSERT INTO tournaments VALUES (default, 't_tour2', 'planned');
INSERT INTO tournaments VALUES (default, 't_tour3', 'ongoing');
INSERT INTO tournaments VALUES (default, 't_tour4', 'ongoing');
INSERT INTO tournaments VALUES (default, 't_tour5', 'closed');
INSERT INTO tournaments VALUES (default, 't_tour6', 'closed');

-- players
INSERT INTO players VALUES (default, 't_player1', 'active');
INSERT INTO players VALUES (default, 't_player2', 'active');
INSERT INTO players VALUES (default, 't_player3', 'active');
INSERT INTO players VALUES (default, 't_player4', 'inactive');
INSERT INTO players VALUES (default, 't_player5', 'inactive');

-- registrations
INSERT INTO registrations VALUES (default, 1, 1); -- T(1); P(1)
INSERT INTO registrations VALUES (default, 1, 2); -- T(1); P(2)
INSERT INTO registrations VALUES (default, 1, 3); -- T(1); P(3)
INSERT INTO registrations VALUES (default, 2, 2); -- T(2); P(2)
INSERT INTO registrations VALUES (default, 2, 3); -- T(2); P(3)
INSERT INTO registrations VALUES (default, 2, 4); -- T(2); P(4)
INSERT INTO registrations VALUES (default, 2, 5); -- T(2); P(5)

-- matches
INSERT INTO matchesRaw VALUES (default, 1, 1, 2, 2, 4); -- T(1); M (1)2:4(2); W(2)
INSERT INTO matchesRaw VALUES (default, 1, 2, 4, 3, 2); -- T(1); M (2)4:2(3); W(2)
INSERT INTO matchesRaw VALUES (default, 1, 1, 4, 3, 2); -- T(1); M (1)4:2(3); W(1)

INSERT INTO matchesRaw VALUES (default, 2, 3, 1, 2, 3); -- T(2); M (3)1:3(2); W(2)
INSERT INTO matchesRaw VALUES (default, 2, 5, 2, 4, 1); -- T(2); M (5)2:1(4); W(5)
INSERT INTO matchesRaw VALUES (default, 2, 5, 0, 2, 2); -- T(2); M (5)0:2(2); W(2)
INSERT INTO matchesRaw VALUES (default, 2, 3, 4, 4, 4); -- T(2); M (3)4:4(4); W( )
