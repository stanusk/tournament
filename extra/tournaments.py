"""Manage a database of tournaments using the Swiss system of organization."""

import psycopg2


# SUPPORTING FUNCTIONS


def connect():
    """Connect to the PostgreSQL 'tournaments' database.

    Returns a database connection.
    """
    return psycopg2.connect("dbname=tournaments")


def countTP(c_type, *status):
    """Count tournaments or players (either all or by status).

    Upon choosing a count type (tournaments or players), return number of all
    tournaments or players if no status is provided, or number of tournaments
    or players of provided status/es.

    Args:
        c_type: String "t" for tournaments or string "p" for players.
        *status: (optional) Name of each selected status as separate string.

    Returns:
        An integer indicating current number of tournaments/players of
        selected status or all tournaments/players in case no status was
        provided.
    """
    types = {
        't': {'status': 'tourStatus', 'view': 'v_toursCount'},
        'p': {'status': 'playerStatus', 'view': 'v_playersCount'}
    }
    if c_type not in types:
        return "Invalid c_type: {0}.".format(c_type)

    db = connect()
    c = db.cursor()

    # List of tuples (one for each option from db tourStatus type) is
    # selected from db.
    c.execute("SELECT "
              "unnest(enum_range(NULL::{0}))".format(types[c_type]['status']))
    db_statuses = [s[0] for s in c.fetchall()]

    # if status is provided, each entry is checked against valid choices from
    # db to ensure valid results as well as to prevent injection (as string
    # formatting is later used for status)
    if status:
        status = [s for s in status]
        for s in status:
            if s not in db_statuses:
                return 'Invalid status: {0}'.format(s)
    # if no status provided, results will reflect all possible choices
    else:
        status = db_statuses

    # Sum up the count of each selected status to get full count of selection.
    c.execute("SELECT sum(count) FROM {0} WHERE status::text = "
              "ANY (ARRAY{1})".format(types[c_type]['view'], status))
    res = c.fetchone()[0]

    c.close()
    db.close()

    return res


def valid_id(table, t_id):
    """Validate if tested id exists in given db table.

    Args:
        table: Complete name of table as string.
        t_id: Tested id as integer.
    Returns:
        boolean: True if id exists in given table, False otherwise.
    """
    db = connect()
    c = db.cursor()
    query = "SELECT id FROM {0} WHERE id = %s".format(table)
    c.execute(query, (t_id,))
    res = c.fetchone()
    c.close()
    db.close()

    if res:
        return True
    return False


def editTP(table, t_id, **kwargs):
    """Change name and/or status of a player or a tournament.

    Args:
        table: Complete name of db table to be updated as string.
        t_id: Id of player/tournament to be edited as integer.
        **kwargs: Either name or status as key='string'
                  (example: name='Dick Somename')
    Returns:
        Upon success, nothing gets returned, but confirmation statement is
        printed. In case of invalid id, error statement gets returned.
    """
    name = kwargs.get('name')
    status = kwargs.get('status')
    # check if provided id is valid
    if valid_id(table, t_id) is False:
        return "Invalid id '{0}'".format(t_id)

    db = connect()
    c = db.cursor()

    # if name was provided, change it in the provided table
    if name:
        # Table is inserted separately as it needs to be inserted without
        # quotes and is not provided by user (thus poses no security risk)
        query = "UPDATE {0} SET name = %s WHERE id = %s".format(table)
        c.execute(query, (name, t_id))
        print ("Name of {0} id '{1}' changed "
               "to '{2}'".format(table[0:-1], t_id, name))
    # if status was provided, change it in the provided table
    if status:
        # Table is inserted separately as it needs to be inserted without
        # quotes and is not provided by user (thus poses no security risk)
        query = "UPDATE {0} SET status = %s WHERE id = %s".format(table)
        c.execute(query, (status, t_id))
        print ("Status {0} id '{1}' changed "
               "to '{2}'".format(table[0:-1], t_id, status))

    db.commit()
    c.close()
    db.close()


# ADMIN FUNCTIONS
# functions used only during testing - not for production


def a_deleteAllTours():
    """Delete all tournaments from table 'tournaments'.

    To be used only by admins for testing purposes as tournaments that are no
    longer active should be marked inactive by changing their status to
    'closed', but never deleted from production environment.
    """
    db = connect()
    c = db.cursor()

    c.execute("DELETE FROM tournaments")

    db.commit()
    c.close()
    db.close()

    print "All tournaments deleted!"


def a_deleteAllPlayers():
    """Delete all players from table 'players'.

    To be used only by admins for testing purposes as players that are no
    longer active should be marked inactive by changing their status to
    'inactive', but never deleted from production environment.
    """
    db = connect()
    c = db.cursor()

    c.execute("DELETE FROM players")

    db.commit()
    c.close()
    db.close()

    print "All players deleted!"


# USER FUNCTIONS


def createNewTour(name):
    """Add a new tournament to table 'tournaments'.

    New tournament is automatically assigned an id (generated by database) and
    by default gets 'planned' status.

    Args:
        name: Complete name of the tournament (need not be unique).
    """
    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO tournaments (name, status) "
              "VALUES (%s, 'planned')", (name, ))
    c.execute("SELECT id FROM tournaments ORDER BY id DESC")

    tour_id = c.fetchone()[0]

    db.commit()
    c.close()
    db.close()

    print "Tournament %s created with the following id: %s" % (name, tour_id)


def changeTourName(t_id, new_name):
    """Change name of tournament in the tournaments table.

    Args:
        t_id: Id of tournament to be edited as string.
        new_name: New complete name of tournament as string.
    """
    editTP('tournaments', t_id, name=new_name)


def changeTourStatus(t_id, new_status):
    """Change status of tournament in the tournaments table.

    Args:
        t_id: Id of tournament to be edited as string.
        new_status: New status of tournament as string.
    """
    editTP('tournaments', t_id, status=new_status)


def countTours(*status):
    """Count tournaments (either all or by status).

    Return number of all tournaments if no status is provided, or number of
    tournaments of provided status/es.

    Args:
        *status: (optional) Name of each selected status as separate string.

    Returns:
        An integer indicating current number of tournaments of selected
        status/es or all tournaments in case no status was provided.
    """
    return countTP('t', *status)


def createNewPlayer(name):
    """Add a new player to table 'players'.

    New player is automatically assigned an id (generated by database) and by
    default gets 'active' status.

    Args:
        name: Full name of the player (need not be unique).
    """
    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO players (name, status) "
              "VALUES (%s, 'active')", (name, ))
    c.execute("SELECT id FROM players ORDER BY id DESC")

    player_id = c.fetchone()[0]

    db.commit()
    c.close()
    db.close()

    print "Player %s created with the following id: %s" % (name, player_id)


def changePlayerName(p_id, new_name):
    """Change name of player in the players table.

    Args:
        p_id: Id of player to be edited as string.
        new_name: New full name of player as string.
    """
    editTP('players', p_id, name=new_name)


def changePlayerStatus(p_id, new_status):
    """Change status of player in the players table.

    Args:
        p_id: Id of player to be edited as string.
        new_status: New status of player as string.
    """
    editTP('players', p_id, status=new_status)


def countPlayers(*status):
    """Count players (either all or by status/es).

    Return number of all players if no status is provided, or number of
    players of provided status/es.

    Args:
        *status: (optional) Name of each selected status as separate string.

    Returns:
        An integer indicating current number of players of selected
        status/es or all players in case no status was provided.
    """
    return countTP('p', *status)
