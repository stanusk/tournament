# Tournament Planner
### [udacity](https://www.udacity.com/) full stack nanodegree project

## Task:
In this project, you’ll be writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

## Basic project objectives:

Written below are basic project requirements, which are fulfilled by files in folder: 'basic'.
For instructions regarding running the program, skip to 'Running the program' section.

**registerPlayer(name)**

Adds a player to the tournament by putting an entry in the database. The database should assign an ID number to the player. Different players may have the same names but will receive different ID numbers.

**countPlayers()**

Returns the number of currently registered players. This function should not use the Python len() function; it should have the database count the players.

**deletePlayers()**

Clear out all the player records from the database.

**reportMatch(winner, loser)**

Stores the outcome of a single match between two players in the database.

**deleteMatches()**

Clear out all the match records from the database.

**playerStandings()**

Returns a list of (id, name, wins, matches) for each player, sorted by the number of wins each player has.

**swissPairings()**

Given the existing set of registered players and the matches they have played, generates and returns a list of pairings according to the Swiss system. Each pairing is a tuple (id1, name1, id2, name2), giving the ID and name of the paired players. For instance, if there are eight registered players, this function should return four pairings. This function should use playerStandings to find the ranking of players.

## Extra credit project objectives:

Written below are extra credit project requirements, which are fulfilled by files in folder: 'extra'.
For instructions regarding running the program, skip to 'Running the program' section.

- Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.
- Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.
- When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
- Support more than one tournament in the database, so matches do not have to be deleted between tournaments. This will require distinguishing between “a registered player” and “a player who has entered in tournament #123”, so it will require changes to the database schema.

**unfulfilled extra credit requirement:**
- Prevent rematches between players.

## System requirements:
- PostgreSQL
- Python 2.7
- (optional) IPython 

## Running the program:

- basic:
```sh
# Clone the git repository and cd into the 'basic' folder of the cloned directory.
git clone https://github.com/stanusk/tournament.git
cd tournament/basic

# run sql to create the database schema
psql -f tournaments.sql

# to run tests, run tournaments_test.py
python tournaments_test.py
# alternatively in ipython:
%run tournaments_test.py

# to use the database, run python/ipython, import tournaments and use functions as documented
python
import tournaments
```

- extra:
```sh
# Clone the git repository and cd into the 'extra' folder of the cloned directory.
git clone https://github.com/stanusk/tournament.git
cd tournament/extra

# run sql to create the database schema
psql -f tournaments.sql

# to run tests, run tournaments_test.py
python tournaments_test.py
# alternatively in ipython:
%run tournaments_test.py

# to use the database, run python/ipython, import tournaments and use functions as documented
python
import tournaments
```
