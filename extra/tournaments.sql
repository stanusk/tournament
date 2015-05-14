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
