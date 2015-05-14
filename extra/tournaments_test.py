"""Test cases for tournament.py."""

from tournaments import *


def testDeleteAllTournaments_a():
    """Test (admin) deleting all tournaments from 'tournaments' table."""
    a_deleteAllTournaments()
    print "###. (adm) Tournaments can be deleted."


def testDeleteAllPlayers_a():
    """Test (admin) deleting all players from 'players' table."""
    a_deleteAllPlayers()
    print "###. (adm) Players can be deleted."


def testCreateNewTournament():
    """Test adding a new tournament to the database."""
    createNewTournament('Knight or Knave')
    print "###. Tournament can be created."


def testCreateNewPlayer():
    """Test adding a new player to the database."""
    createNewPlayer('Steve Jobs')
    print "###. Player can be created."


if __name__ == '__main__':
    testDeleteAllTournaments_a()
    testDeleteAllPlayers_a()
    testCreateNewTournament()
    testCreateNewPlayer()
    print "All tests passed successfully!"
