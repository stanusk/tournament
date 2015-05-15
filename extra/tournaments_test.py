"""Test cases for tournament.py."""

from tournaments import *


def testDeleteAllTours_a():
    """Test (admin) deleting all tournaments from 'tournaments' table."""
    a_deleteAllTours()
    print "###. (adm) Success: tournaments can be deleted."


def testDeleteAllPlayers_a():
    """Test (admin) deleting all players from 'players' table."""
    a_deleteAllPlayers()
    print "###. (adm) Success: players can be deleted."


def testCreateNewTour():
    """Test adding a new tournament to the database."""
    a_deleteAllTours()
    createNewTour('Knight or Knave')
    print "###. Success: tournament can be created."


def testCreateNewPlayer():
    """Test adding a new player to the database."""
    a_deleteAllPlayers()
    createNewPlayer('Steve Jobs')
    print "###. Success: player can be created."


def testEditPlayer():
    """Test changing player name and status."""
    a_deleteAllPlayers()
    # create test player
    createNewPlayer("Elon Musk")
    db = connect()
    c = db.cursor()
    # get test player id
    c.execute("SELECT id FROM players WHERE name = 'Elon Musk'")
    p_id = c.fetchone()[0]
    # edit test player
    changePlayerName(p_id, "Nikola Tesla")
    changePlayerStatus(p_id, "inactive")
    # get changed name and status
    c.execute("SELECT name, status FROM players WHERE id = %s", (p_id,))
    p_details = c.fetchone()
    c.close()
    db.close()
    # compare new name and status to the desired ones
    if p_details[0] == "Nikola Tesla":
        print "###. Success: player name changed."
    else:
        raise ValueError("changePlayerName() failed to change player's name")
    if p_details[1] == "inactive":
        print "###. Success: player status changed."
    else:
        raise ValueError("changePlayerStatus() failed to change player's "
                         "status")


def testEditTour():
    """Test changing tournament name and status."""
    a_deleteAllTours()
    # create test tournament
    createNewTour("Metlobal")
    db = connect()
    c = db.cursor()
    # get test tournament id
    c.execute("SELECT id FROM tournaments WHERE name = 'Metlobal'")
    t_id = c.fetchone()[0]
    # edit test tournament
    changeTourName(t_id, "Beer-pong")
    changeTourStatus(t_id, "ongoing")
    # get changed name and status
    c.execute("SELECT name, status FROM tournaments WHERE id = %s", (t_id,))
    t_details = c.fetchone()
    c.close()
    db.close()
    # compare new name and status to the desired ones
    if t_details[0] == "Beer-pong":
        print "###. Success: tournament name changed."
    else:
        raise ValueError("changeTourName() failed to change tournament's name")
    if t_details[1] == "ongoing":
        print "###. Success: tournament status changed."
    else:
        raise ValueError("changeTourStatus() failed to change tournament's "
                         "status")


def testCountToursAll():
    """Test counting all tournaments."""
    a_deleteAllTours()
    createNewTour("Knight on Knave")
    createNewTour("CheckiO World Championship")
    count = countTours()
    if count != 2:
        raise ValueError("countTours() should return numeric 2")
    else:
        print "###. Success: countTours() returned numeric 2."


def testCountToursClosed():
    """Test counting closed tournaments."""
    a_deleteAllTours()
    createNewTour("Knight on Knave")
    createNewTour("CheckiO World Championship")
    db = connect()
    c = db.cursor()
    # get test tournament id
    c.execute("SELECT id FROM tournaments WHERE name = 'Knight on Knave'")
    t_id = c.fetchone()[0]
    c.close()
    db.close()
    changeTourStatus(t_id, "closed")
    count = countTours("closed")
    if count != 1:
        raise ValueError("countTours('closed') should return numeric 1")
    else:
        print "###. Success: countTours('closed') returned numeric 1."


def testCountPlayersAll():
    """Test counting all players."""
    a_deleteAllPlayers()
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    count = countPlayers()
    if count != 2:
        raise ValueError("countPlayers() should return numeric 2")
    else:
        print "###. Success: countPlayers() returned numeric 2."


def testCountPlayersInactive():
    """Test counting inactive players."""
    a_deleteAllPlayers()
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    db = connect()
    c = db.cursor()
    # get test player id
    c.execute("SELECT id FROM players WHERE name = 'Bill Gates'")
    p_id = c.fetchone()[0]
    c.close()
    db.close()
    changePlayerStatus(p_id, "inactive")
    count = countPlayers("inactive")
    if count != 1:
        raise ValueError("countPlayers('inactive') should return numeric 1")
    else:
        print "###. Success: countPlayers('inactive') returned numeric 1."


if __name__ == '__main__':
    testDeleteAllTours_a()
    testDeleteAllPlayers_a()
    testCreateNewTour()
    testCreateNewPlayer()
    testEditTour()
    testEditPlayer()
    testCountToursAll()
    testCountPlayersAll()
    testCountToursClosed()
    testCountPlayersInactive()
    print "All tests passed successfully!"
