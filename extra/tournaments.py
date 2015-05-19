"""Manage a database of tournaments using the Swiss system of organization."""

import psycopg2


# SUPPORTING FUNCTIONS


def s_connect():
    """Connect to the PostgreSQL 'tournaments' database.

    Returns a database connection.
    """
    return psycopg2.connect("dbname=tournaments")


def s_countTP(c_type, *status):
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
        't': {'status': 'tourStatus', 'view': 'v_toursCountByStatus'},
        'p': {'status': 'playerStatus', 'view': 'v_playersCountByStatus'}
    }
    if c_type not in types:
        print "Invalid c_type: '{0}'!".format(c_type)
        return None

    db = s_connect()
    c = db.cursor()

    # List valid statuses from the db
    c.execute("SELECT "
              "unnest(enum_range(NULL::{0}))".format(types[c_type]['status']))
    db_statuses = [s[0] for s in c.fetchall()]

    # If status is provided, each entry is checked against valid choices from
    # db to ensure valid results as well as to prevent injection (as string
    # formatting is later used for status).
    if status:
        status = [s for s in status]
        for s in status:
            if s not in db_statuses:
                print "Invalid status: '{0}'!".format(s)
                return None
    # If no status provided, results will reflect all possible choices.
    else:
        status = db_statuses

    # Sum up the count of all selected statuses to get full count of selection.
    c.execute("SELECT sum(count) FROM {0} WHERE status::text = "
              "ANY (ARRAY{1})".format(types[c_type]['view'], status))
    res = c.fetchone()[0]

    c.close()
    db.close()

    return res


def s_validId(table, r_id):
    """Validate if tested id exists in given db table.

    Args:
        table: Complete name of table as string.
        r_id: Tested record id as integer.
    Returns:
        boolean: True if id exists in given table, False otherwise.
    """
    db = s_connect()
    c = db.cursor()
    query = "SELECT id FROM {0} WHERE id = %s".format(table)
    c.execute(query, (r_id,))
    res = c.fetchone()
    c.close()
    db.close()

    if res:
        return True
    return False


def s_editTP(table, r_id, **kwargs):
    """Change name and/or status of a player or a tournament.

    Args:
        table: Complete name of db table to be updated as string.
        r_id: ID of record (player/tournament) to be edited as integer.
        **kwargs: Either name or status as key='string'
                  (example: name='Dick Somename')
    Returns:
        Upon success, nothing gets returned, but confirmation statement is
        printed. In case of invalid id, error statement gets returned.
    """
    name = kwargs.get('name')
    status = kwargs.get('status')
    # check if provided id is valid
    if s_validId(table, r_id) is False:
        print "Invalid id '{0}'!".format(r_id)
        return None

    db = s_connect()
    c = db.cursor()

    # if name was provided, change it in the provided table
    if name:
        # Table is inserted separately as it needs to be inserted without
        # quotes and is not provided by user (thus poses no security risk)
        query = "UPDATE {0} SET name = %s WHERE id = %s".format(table)
        c.execute(query, (name, r_id))
        print ("Name of {0} id '{1}' changed "
               "to '{2}'".format(table[0:-1], r_id, name))
    # if status was provided, change it in the provided table
    if status:
        # Table is inserted separately as it needs to be inserted without
        # quotes and is not provided by user (thus poses no security risk)
        query = "UPDATE {0} SET status = %s WHERE id = %s".format(table)
        c.execute(query, (status, r_id))
        print ("Status of {0} id '{1}' changed "
               "to '{2}'".format(table[0:-1], r_id, status))

    db.commit()
    c.close()
    db.close()


def s_getStatusById(table, r_id):
    """Return status of record with provided id from provided db table.

    Args:
        table: Complete name of db table to be searched for status.
        r_id: ID of record (player/tournament) as integer.
    Returns:
        Status of record as string.
    """
    db = s_connect()
    c = db.cursor()
    # Table is inserted separately as it needs to be inserted without
    # quotes and is not provided by user (thus poses no security risk)
    query = "SELECT status FROM {0} WHERE id = %s".format(table)
    c.execute(query, (r_id,))
    res = c.fetchone()[0]
    c.close()
    db.close()
    return res


# ADMIN FUNCTIONS
# functions used only during testing - not for production


def a_deleteAllTours():
    """Delete all data from table 'tournaments'.

    To be used only by admins for testing purposes as tournaments that are no
    longer active should be marked inactive by changing their status to
    'closed', but never deleted from production environment.
    """
    db = s_connect()
    c = db.cursor()

    c.execute("DELETE FROM tournaments")

    db.commit()
    c.close()
    db.close()

    print "All tournaments deleted."


def a_deleteAllPlayers():
    """Delete all data from table 'players'.

    To be used only by admins for testing purposes as players that are no
    longer active should be marked inactive by changing their status to
    'inactive', but never deleted from production environment.
    """
    db = s_connect()
    c = db.cursor()

    c.execute("DELETE FROM players")

    db.commit()
    c.close()
    db.close()

    print "All players deleted."


def a_deleteAllRegistrations():
    """Delete all data from table 'registrations'.

    To be used only by admins for testing purposes as users should not be
    allowed to delete more than one player or tournament from table
    'registrations' at a time.
    """
    db = s_connect()
    c = db.cursor()

    c.execute("DELETE FROM registrations")

    db.commit()
    c.close()
    db.close()

    print "All registrations deleted."


# USER FUNCTIONS


# MAINTENANCE OF TABLE: tournaments

def createNewTour(name):
    """Add a new tournament to table 'tournaments'.

    New tournament is automatically assigned an id (generated by database) and
    by default gets 'planned' status.

    Args:
        name: Complete name of the tournament (need not be unique).
    """
    db = s_connect()
    c = db.cursor()

    c.execute("INSERT INTO tournaments (name, status) "
              "VALUES (%s, 'planned')", (name, ))
    c.execute("SELECT id FROM tournaments ORDER BY id DESC")

    tour_id = c.fetchone()[0]

    db.commit()
    c.close()
    db.close()

    print ("Tournament '{0}' created with the following "
           "id: '{1}'.".format(name, tour_id))


def changeTourName(t_id, new_name):
    """Change name of tournament in the tournaments table.

    Args:
        t_id: ID of tournament to be edited as string.
        new_name: New complete name of tournament as string.
    """
    s_editTP('tournaments', t_id, name=new_name)


def changeTourStatus(t_id, new_status):
    """Change status of tournament in the tournaments table.

    Args:
        t_id: ID of tournament to be edited as string.
        new_status: New status of tournament as string.
    """
    s_editTP('tournaments', t_id, status=new_status)


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
    return s_countTP('t', *status)


# MAINTENANCE OF TABLE: players

def createNewPlayer(name):
    """Add a new player to table 'players'.

    New player is automatically assigned an id (generated by database) and by
    default gets 'active' status.

    Args:
        name: Full name of the player (need not be unique).
    """
    db = s_connect()
    c = db.cursor()

    c.execute("INSERT INTO players (name, status) "
              "VALUES (%s, 'active')", (name, ))
    c.execute("SELECT id FROM players ORDER BY id DESC")

    p_id = c.fetchone()[0]

    db.commit()
    c.close()
    db.close()

    print ("Player '{0}' created with the following "
           "id: '{1}'.".format(name, p_id))


def changePlayerName(p_id, new_name):
    """Change name of player in the players table.

    Args:
        p_id: ID of player to be edited as string.
        new_name: New full name of player as string.
    """
    s_editTP('players', p_id, name=new_name)


def changePlayerStatus(p_id, new_status):
    """Change status of player in the players table.

    Args:
        p_id: ID of player to be edited as string.
        new_status: New status of player as string.
    """
    s_editTP('players', p_id, status=new_status)


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
    return s_countTP('p', *status)


# MAINTENANCE OF TABLE: registrations

def registerPlayers(t_id, *p_id):
    """Register one or multiple players for provided tournament.

    Args:
        t_id: ID number of tournament for which players are being
                 registered as integer
        *p_id: ID number for each player to be registered for a provided
                    tournament.
    """
    # Check if provided id is valid.
    if s_validId('tournaments', t_id) is False:
        print "Invalid id '{0}'!".format(t_id)
        return None
    # Check if tournament is of status 'planned' (users should not be able to
    # register new players to ongoing or closed tournaments)
    if s_getStatusById('tournaments', t_id) != 'planned':
        print ("Unable to register for tournament id '{0}'! Tournament no "
               "longer in 'planned' phase.".format(t_id))
        return None
    db = s_connect()
    c = db.cursor()
    for p in p_id:
        # Check if provided id is valid.
        if s_validId('players', p) is False:
            print "Invalid player id '{0}'!".format(p)
            continue
        # Check if player is of status 'active'.
        if s_getStatusById('players', p) != 'active':
            print ("Unable to register player id '{0}'! Player "
                   "inactive.".format(p))
            continue
        # If both checks passed, register player
        c.execute("INSERT INTO registrations VALUES (default, %s, %s)",
                  (t_id, p))
        print ("Player id '{0}' registered for tournament "
               "id '{1}'".format(p, t_id))
    db.commit()
    c.close()
    db.close()
