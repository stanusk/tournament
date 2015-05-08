#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()

    c.execute("DELETE FROM matches")

    db.commit()
    db.close()

    print "all match records deleted"


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()

    c.execute("DELETE FROM players")

    db.commit()
    db.close()

    print "all player records deleted"


def countPlayers():
    """Return the number of players currently registered."""
    db = connect()
    c = db.cursor()

    c.execute("SELECT count(*) FROM players")
    res = c.fetchone()[0]

    db.close()

    return res


def registerPlayer(name):
    """Add a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Assuming that players are added only in case that they are supposed to
    enroll in the tournament, each player is automatically added to both:
    players table and matches (where the player is assigned id identical to
    id in players table, 0 value for wins and 0 value for matches played)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO players (name) VALUES (%s)", (name, ))

    c.execute("SELECT id FROM players ORDER BY id DESC")
    latest_id = c.fetchone()
    c.execute("INSERT INTO matches VALUES (%s, 0, 0)", (latest_id, ))

    db.commit()
    db.close()

    print "player %s successfully registered" % (name)


def playerStandings():
    """Return a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()

    c.execute("SELECT * FROM standings")
    res = c.fetchall()

    db.close()

    return res


def reportMatch(winner, loser):
    """Record the outcome of a single match between two players.

    Assuming that tie is not an option, both winner and loser get their
    number of matches increased by 1 and the winner gets number of wins
    increased by 1.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()

    c.execute(
        "UPDATE matches SET matches = matches + 1 "
        "WHERE player_id = %s OR player_id = %s", (winner, loser, )
        )
    c.execute(
        "UPDATE matches SET wins = wins + 1 "
        "WHERE player_id = %s", (winner, )
        )

    db.commit()
    db.close()

    print "results uploaded"


def swissPairings():
    """Return a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()

    c.execute("SELECT id, name FROM standings")
    all_players = c.fetchall()

    db.close()

    res = []
    while all_players:
        res.append(all_players[0]+all_players[1])
        del all_players[0:2]

    return res
