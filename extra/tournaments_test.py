"""Test cases for tournament.py."""

from tournaments import *


def testDeleteAllTournaments_a():
    """Test (admin) deleting all tournaments from 'tournaments' table."""
    a_deleteAllTournaments()
    print "###. (adm) Success: tournaments can be deleted."


def testDeleteAllPlayers_a():
    """Test (admin) deleting all players from 'players' table."""
    a_deleteAllPlayers()
    print "###. (adm) Success: players can be deleted."


def testCreateNewTournament():
    """Test adding a new tournament to the database."""
    createNewTournament('Knight or Knave')
    print "###. Success: tournament can be created."


def testCountToursAll():
    """Test counting all tournaments."""
    a_deleteAllTournaments()
    createNewTournament("Knight on Knave")
    createNewTournament("CheckiO World Championship")
    count = countTournaments()
    if count != 2:
        raise ValueError("countTournaments() should return numeric 2")
    else:
        print "###. Success: countTournaments() returned numeric 2."


def testCreateNewPlayer():
    """Test adding a new player to the database."""
    createNewPlayer('Steve Jobs')
    print "###. Success: player can be created."


if __name__ == '__main__':
    testDeleteAllTournaments_a()
    testDeleteAllPlayers_a()
    testCreateNewTournament()
    testCountToursAll()
    testCreateNewPlayer()
    print "All tests passed successfully!"
