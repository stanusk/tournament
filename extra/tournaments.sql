/* PostgreSQL database for Swiss style tournament. */


/* Create db */

DROP DATABASE tournaments;
CREATE DATABASE tournaments;
\c tournaments


/* Establish schema */

-- DATA TYPES --
CREATE TYPE tourStatus AS ENUM ('planned', 'ongoing', 'closed');
CREATE TYPE playerStatus AS ENUM ('active', 'inactive');


-- TABLES --
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
    -- each player can be registered only once for given tournament
    UNIQUE (tour_id, player_id)
);

CREATE TABLE matchesRaw (
    id serial PRIMARY KEY,
    tour_id int NOT NULL,
    pl1_id int NOT NULL,
    pl1_score int NOT NULL,
    pl2_id int NOT NULL,
    pl2_score int NOT NULL,
    -- ON DELETE CASCADE is set to simplify testing since deleting is
    -- restricted to admins (for testing only)
    FOREIGN KEY (tour_id, pl1_id) REFERENCES registrations(tour_id, player_id) ON DELETE CASCADE,
    FOREIGN KEY (tour_id, pl2_id) REFERENCES registrations(tour_id, player_id) ON DELETE CASCADE
);


-- VIEWS --

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
CREATE VIEW v_matches AS
    SELECT *,
            -- add winner: select id of player with higher score as winner or id of player with assigned bye as winner or leave empty (null) in case of a draw
            CASE WHEN pl1_score > pl2_score THEN pl1_id
                 WHEN pl1_score < pl2_score THEN pl2_id
                 WHEN pl1_id = pl2_id THEN pl1_id -- bye case
            END AS winner_id
    FROM matchesRaw;

-- function for creating a view of opponents of a given player in a given tournament
CREATE OR REPLACE FUNCTION opponents(tour_id int, player_id int)
    RETURNS table (opponenets int)
    AS
    $body$
        SELECT CASE WHEN pl1_id = $2 THEN pl2_id
                    WHEN pl2_id = $2 THEN pl1_id
               END
        FROM v_matches
        WHERE tour_id = $1 AND pl1_id != pl2_id AND (pl1_id = $2 OR pl2_id = $2)
    $body$
    language sql;

CREATE VIEW v_tourStandings AS
    SELECT r.tour_id,
           r.player_id,
           -- name matched from players table
           (SELECT name FROM players WHERE id = r.player_id),
           -- matches played: count of IDs from v_matches with matching tour_id and player_id (either as player 1 or player 2)
           (SELECT count(id) AS matches FROM v_matches WHERE tour_id = r.tour_id AND (pl1_id = r.player_id OR pl2_id = r.player_id)),
           -- wins: count of winner_IDs from v_matches with matching tour_id where given player_id equals winner_id
           (SELECT count(winner_id) AS wins FROM v_matches WHERE tour_id = r.tour_id AND winner_id = r.player_id),
           -- draws: count of IDs from v_matches with matching tour_id and player_id (either as player 1 or player 2) where winner_id is null
           (SELECT count(id) AS draws FROM v_matches WHERE tour_id = r.tour_id AND (pl1_id = r.player_id OR pl2_id = r.player_id) AND winner_id IS NULL),
           -- byes: count of IDs from v_matches with matching tour_id where player 1 equals player 2
           (SELECT count(id) AS byes FROM v_matches WHERE tour_id = r.tour_id AND pl1_id = r.player_id AND pl1_id = pl2_id),
           -- omw (opponent match wins): sum of wins of all opponents of given player within given tournament
           (SELECT sum(wins) as omw
            FROM (
                -- winners with number of wins by tournament
                SELECT tour_id, winner_id, count(winner_id) AS wins 
                FROM v_matches 
                WHERE winner_id IS NOT NULL 
                GROUP BY tour_id, winner_id
            ) AS wins
            WHERE tour_id = r.tour_id AND winner_id IN (
                -- opponents of r.player_id
                SELECT * FROM opponents(r.tour_id, r.player_id)
                -- SELECT CASE WHEN pl1_id = r.player_id THEN pl2_id
                --             WHEN pl2_id = r.player_id THEN pl1_id
                --        END
                -- FROM v_matches
                -- -- exclude byes
                -- WHERE pl1_id != pl2_id
            ))
    FROM registrations AS r
    ORDER BY r.tour_id, wins DESC, draws DESC, omw DESC;


/* Populate db */
-- for ad hoc tests during db design

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
INSERT INTO matchesRaw VALUES (default, 1, 3, 0, 3, 0); -- T(1); M (3)0:0(3); W(3)
INSERT INTO matchesRaw VALUES (default, 1, 2, 4, 3, 2); -- T(1); M (2)4:2(3); W(2)
INSERT INTO matchesRaw VALUES (default, 1, 1, 0, 1, 0); -- T(1); M (1)0:0(1); W(1)
INSERT INTO matchesRaw VALUES (default, 1, 1, 4, 3, 2); -- T(1); M (1)4:2(3); W(1)
INSERT INTO matchesRaw VALUES (default, 1, 2, 0, 2, 0); -- T(1); M (2)0:0(2); W(2)

INSERT INTO matchesRaw VALUES (default, 2, 3, 1, 2, 3); -- T(2); M (3)1:3(2); W(2)
INSERT INTO matchesRaw VALUES (default, 2, 5, 2, 4, 1); -- T(2); M (5)2:1(4); W(5)
INSERT INTO matchesRaw VALUES (default, 2, 5, 0, 2, 2); -- T(2); M (5)0:2(2); W(2)
INSERT INTO matchesRaw VALUES (default, 2, 3, 4, 4, 4); -- T(2); M (3)4:4(4); W( )
