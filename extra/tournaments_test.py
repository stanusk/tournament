"""Test cases for tournament.py."""

from tournaments import *


# SUPPORTING FUNCTIONS

def t_getIdByName(table, name):
    """Return id by name in given db table.

    Retrieve an id of a player or a tournament with the provided name from
    the provided table (players / tournaments).

    Args:
        table: Complete name of table as string.
        name: Complete name of tournament or player as string.
    Returns:
        An integer referencing the id of provided player/tournament in the
        provided table.
    """
    db = s_connect()
    c = db.cursor()
    # order by name to enable reusing names without the need to delete all
    # data from the database for each new test case
    c.execute("SELECT id FROM {0} WHERE name = '{1}' "
              "ORDER BY id DESC".format(table, name))
    t_id = c.fetchone()[0]
    c.close()
    db.close()
    return t_id


# TEST FUNCTIONS

def testDeleteAllTours_a():
    """Test (admin) deleting all tournaments from 'tournaments' table."""
    a_deleteAllTours()
    print "1. (adm) Success: tournaments can be deleted."


def testDeleteAllPlayers_a():
    """Test (admin) deleting all players from 'players' table."""
    a_deleteAllPlayers()
    print "2. (adm) Success: players can be deleted."


def testCreateNewTour():
    """Test adding a new tournament to the database."""
    createNewTour('Knight or Knave')
    print "3. Success: tournament can be created."


def testCreateNewPlayer():
    """Test adding a new player to the database."""
    createNewPlayer('Steve Jobs')
    print "4. Success: player can be created."


def testEditPlayer():
    """Test changing player name and status."""
    # create test player
    createNewPlayer("Elon Musk")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')

    # edit test player
    changePlayerName(p_id, "Nikola Tesla")
    changePlayerStatus(p_id, "inactive")

    db = s_connect()
    c = db.cursor()
    # get changed name and status
    c.execute("SELECT name, status FROM players WHERE id = %s", (p_id,))
    p_details = c.fetchone()
    c.close()
    db.close()
    # compare new name and status to the desired ones
    if p_details[0] == "Nikola Tesla":
        print "5a. Success: player name changed."
    else:
        raise ValueError("changePlayerName() failed to change player's name")
    if p_details[1] == "inactive":
        print "5b. Success: player status changed."
    else:
        raise ValueError("changePlayerStatus() failed to change player's "
                         "status")


def testEditTour():
    """Test changing tournament name and status."""
    # create test tournament
    createNewTour("Metlobal")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Metlobal')

    # edit test tournament
    changeTourName(t_id, "Beer-pong")
    changeTourStatus(t_id, "ongoing")

    db = s_connect()
    c = db.cursor()
    # get changed name and status
    c.execute("SELECT name, status FROM tournaments WHERE id = %s", (t_id,))
    t_details = c.fetchone()
    c.close()
    db.close()
    # compare new name and status to the desired ones
    if t_details[0] == "Beer-pong":
        print "6a. Success: tournament name changed."
    else:
        raise ValueError("changeTourName() failed to change tournament's name")
    if t_details[1] == "ongoing":
        print "6b. Success: tournament status changed."
    else:
        raise ValueError("changeTourStatus() failed to change tournament's "
                         "status")


def testCountToursAll():
    """Test counting all tournaments."""
    a_deleteAllTours()
    # create test tournaments
    createNewTour("Knight on Knave")
    createNewTour("CheckiO World Championship")
    c = countTours()
    if c != 2:
        raise ValueError("countTours() should return numeric 2")
    else:
        print "7. Success: countTours() returned numeric 2."


def testCountToursClosed():
    """Test counting closed tournaments."""
    a_deleteAllTours()
    # create test tournaments
    createNewTour("Knight on Knave")
    createNewTour("CheckiO World Championship")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight on Knave')
    # change status of test tournament to "closed"
    changeTourStatus(t_id, "closed")
    # count "closed" tournaments
    c = countTours("closed")
    if c != 1:
        raise ValueError("countTours('closed') should return numeric 1")
    else:
        print "8. Success: countTours('closed') returned numeric 1."


def testCountPlayersAll():
    """Test counting all players."""
    a_deleteAllPlayers()
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    c = countPlayers()
    if c != 2:
        raise ValueError("countPlayers() should return numeric 2")
    else:
        print "9. Success: countPlayers() returned numeric 2."


def testCountPlayersInactive():
    """Test counting inactive players."""
    a_deleteAllPlayers()
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Bill Gates')
    # change test players status to "inactive"
    changePlayerStatus(p_id, "inactive")
    # count players with "inactive" status
    c = countPlayers("inactive")
    if c != 1:
        raise ValueError("countPlayers('inactive') should return numeric 1")
    else:
        print "10. Success: countPlayers('inactive') returned numeric 1."


def testDeleteAllRegistrations():
    """Test (admin) deleting all registrations."""
    a_deleteAllRegistrations()
    print "11. (adm) Success: registrations can be deleted."


def testRegisterOnePlayer():
    """Test registering a player for a tournament."""
    # create test player
    createNewPlayer("Elon Musk")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')

    # register player
    registerPlayers(t_id, p_id)

    db = s_connect()
    c = db.cursor()
    c.execute("SELECT player_id FROM registrations "
              "WHERE tour_id = %s", (t_id,))
    res = c.fetchone()[0]
    if res != p_id:
        raise ValueError("Player %s failed to be registered." % (p_id))
    else:
        print ("12. Success: player id %s registered "
               "for tournament id %s." % (p_id, t_id))


def testCountRegisteredPlayers():
    """Test counting players registered for given tournament."""
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    p2_id = p_id + 1
    # create test tournaments
    createNewTour("Knight or Knave")
    createNewTour("World Domination")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    t2_id = t_id + 1
    # register players - each to separate tournament
    registerPlayers(t_id, p_id)
    registerPlayers(t2_id, p2_id)

    # count players registered to first created tournament
    c = countRegPlayers(t_id)
    if c != 1:
        raise ValueError("countRegPlayers(t_id) should return numeric 1")
    else:
        print "13. Success: countRegPlayers(t_id) returned numeric 1."


def testRegisterMultiplePlayers():
    """Test registering multiple players for a tournament."""
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    p2_id = p_id + 1
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')

    # register multiple players to provided tournament
    registerPlayers(t_id, p_id, p2_id)

    # count players registered to the tournament
    c = countRegPlayers(t_id)
    if c != 2:
        raise ValueError("countRegPlayers(t_id) should return numeric 2")
    else:
        print "14. Success: multiple players registered."


def testDeregisterAllPlayers():
    """Test deregistering all players of provided tournament."""
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    p2_id = p_id + 1
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    # register all players to provided tournament
    registerPlayers(t_id, p_id, p2_id)
    # deregister all players from provided tournament
    deregisterPlayers(t_id)
    # count players registered to the tournament
    c = countRegPlayers(t_id)
    if c != 0:
        raise ValueError("countRegPlayers(t_id) should return numeric 0")
    else:
        print "15. Success: all players deregistered."


def testDeregisterProvidedPlayers():
    """Test deregistering all players of provided tournament."""
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    p2_id = p_id + 1
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    # register all players to provided tournament
    registerPlayers(t_id, p_id, p2_id)
    # deregister first player from provided tournament
    deregisterPlayers(t_id, p_id)
    # count players registered to the tournament
    c = countRegPlayers(t_id)
    if c != 1:
        raise ValueError("countRegPlayers(t_id) should return numeric 1")
    else:
        print "16. Success: provided players deregistered."


def testStandingsBeforeMatches():
    """Test obtaining tournament standings before any matches are played."""
    # create test players
    createNewPlayer("Elon Musk")
    createNewPlayer("Bill Gates")
    # get test player id
    p_id = t_getIdByName('players', 'Elon Musk')
    p2_id = p_id + 1
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    # register all players to provided tournament
    registerPlayers(t_id, p_id, p2_id)
    standings = tournamentStandings(t_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even"
                         " before they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in "
                         "standings.")
    if len(standings[0]) != 8:
        raise ValueError("Each playerStandings row should have eight "
                         "columns.")
    [(t_id, id1, name1, matches1, wins1, draws1, byes1, omw1),
     (t_id, id2, name2, matches2, wins2, draws2, byes2, omw2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Elon Musk", "Bill Gates"]):
        raise ValueError("Registered players' names should appear in "
                         "standings, even if they have no matches played.")
    print ("17. Success: newly registered players appear in the standings "
           "with no matches.")


def testReportMatches():
    """Test reporting matches including wins, byes, draws.

    Test includes check for general order in which players should be after
    simulated rounds in the standings.
    """
    players = ["Elon Musk", "Bruno Walton", "Boots O'Neal", "Cathy Burton",
               "Diane Grant"]
    # create test players
    for p in players:
        createNewPlayer(p)
    # get test player IDs
    p1_id = t_getIdByName('players', 'Elon Musk')
    p2_id, p3_id, p4_id, p5_id = p1_id + 1, p1_id + 2, p1_id + 3, p1_id + 4
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    # register all players to provided tournament
    registerPlayers(t_id, p1_id, p2_id, p3_id, p4_id, p5_id)

    changeTourStatus(t_id, "ongoing")
    reportMatch(t_id, p1_id, 6, p2_id, 3)  # w(1)
    reportMatch(t_id, p3_id, 1, p4_id, 3)  # w(4)
    reportMatch(t_id, p5_id, 0, p5_id, 0)  # w(5) - bye

    reportMatch(t_id, p1_id, 2, p4_id, 1)  # w(1)
    reportMatch(t_id, p2_id, 0, p2_id, 0)  # w(2) - bye
    reportMatch(t_id, p3_id, 3, p5_id, 3)  # w( ) - draw

    reportMatch(t_id, p1_id, 0, p5_id, 1)  # w(5)
    reportMatch(t_id, p4_id, 4, p2_id, 3)  # w(4)
    reportMatch(t_id, p3_id, 0, p3_id, 0)  # w(3) - bye

    standings = tournamentStandings(t_id)

    pos = 0  # used in loop below to identify player's position in standings
    for (t, i, n, m, w, d, b, o) in standings:

        if i == p1_id and (m, w, d, b, o) != (3, 2, 0, 0, 5):
            raise ValueError("Elon should have 3 matches, 2 wins, 0 draws, "
                             "0 byes, 5 OMWs")
        if i == p2_id and (m, w, d, b, o) != (3, 1, 0, 1, 4):
            raise ValueError("Bruno should have 3 matches, 1 win, 0 draws, "
                             "1 bye, 4 OMWs")
        if i == p3_id and (m, w, d, b, o) != (3, 1, 1, 1, 4):
            raise ValueError("Boots should have 3 matches, 1 win, 1 draw, "
                             "1 bye, 4 OMWs")
        if i == p4_id and (m, w, d, b, o) != (3, 2, 0, 0, 4):
            raise ValueError("Cathy should have 3 matches, 2 wins, 0 draws, "
                             "0 byes, 4 OMWs")
        if i == p5_id and (m, w, d, b, o) != (3, 2, 1, 1, 3):
            raise ValueError("Diane should have 3 matches, 2 wins, 1 draw, "
                             "1 bye, 3 OMWs")

        res = [p5_id, p1_id, p4_id, p3_id, p2_id]
        if i != res[pos]:
            raise ValueError("Player standings order is wrong for: "
                             "{0}.".format(i))
        pos += 1

    print "18. Success: after a tournament, players have correct standings."


def testPairings():
    """Test swiss pairings."""
    players = ["Twilight Sparkle", "Fluttershy", "Applejack", "Pinkie Pie"]
    # create test players
    for p in players:
        createNewPlayer(p)
    # get test player IDs
    p1_id = t_getIdByName('players', 'Twilight Sparkle')
    p2_id, p3_id, p4_id = p1_id + 1, p1_id + 2, p1_id + 3
    # create test tournament
    createNewTour("Knight or Knave")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Knight or Knave')
    # register all players to provided tournament
    registerPlayers(t_id, p1_id, p2_id, p3_id, p4_id)
    changeTourStatus(t_id, "ongoing")
    reportMatch(t_id, p1_id, 6, p2_id, 3)  # w(1)
    reportMatch(t_id, p3_id, 6, p4_id, 3)  # w(4)

    pairings = swissPairings(t_id)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([p1_id, p3_id]), frozenset([p2_id, p4_id])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "19. Success: after one match, players with one win are paired."


def testPairingsOdd():
    """Test swiss pairings with odd number of players."""
    players = ["Jack Sparrow", "Fluttershy",
               "Applejack", "Pinkie Pie", "Peter Pan"]
    # create test players
    for p in players:
        createNewPlayer(p)
    # get test player IDs
    p1_id = t_getIdByName('players', 'Jack Sparrow')
    p2_id, p3_id, p4_id, p5_id = p1_id + 1, p1_id + 2, p1_id + 3, p1_id + 4
    # create test tournament
    createNewTour("Give a Jack")
    # get test tournament id
    t_id = t_getIdByName('tournaments', 'Give a Jack')
    # register all players to provided tournament
    registerPlayers(t_id, p1_id, p2_id, p3_id, p4_id, p5_id)
    changeTourStatus(t_id, "ongoing")

    pairings = swissPairings(t_id)
    if len(pairings) != 3:
        raise ValueError(
            "For five players, swissPairings should return three pairs.")
    print "20. Success: all five players paired."


# TESTS

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
    testDeleteAllRegistrations()
    testRegisterOnePlayer()
    testCountRegisteredPlayers()
    testRegisterMultiplePlayers()
    testDeregisterAllPlayers()
    testDeregisterProvidedPlayers()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testPairingsOdd()
    print "All tests passed successfully!"
