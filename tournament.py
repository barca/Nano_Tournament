#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

#connects to db
def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")
#deltes match records from database 
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM history;")
    c.execute("UPDATE matches SET wins = 0;")
    conn.commit()
#remove just the players
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    c.execute("DELETE FROM history")
    conn.commit()
#returns number of players
def countPlayers():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT (*) FROM matches;")
    count = c.fetchall()
    conn.commit()
    return count[0][0]
    """Returns the number of players currently registered."""

#adds player to db, with 0 wins, and 0 matches already played
def registerPlayer(name):
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (name, wins, matches) VALUES  (%s, %s, %s)",(name,0,0,))
    conn.commit()

    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

#returns a playerlist, sorted by wins in decending order
def playerStandings():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name, wins, matches FROM matches ORDER BY wins DESC")
    players = c.fetchall()
    conn.commit()
    return players

    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

#follows spec, adds match winner and loser, increments match number
def reportMatch(winner, loser):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT wins FROM matches WHERE id = ('%s')",(winner,))
    wins = c.fetchall()
    wins = wins[0][0] +  1
    c.execute("SELECT matches FROM matches WHERE id = ('%s')",(winner,))
    matches = c.fetchall()
    matches = matches[0][0] +  1
    c.execute("UPDATE matches set wins = ('%s') WHERE id = ('%s')",(wins,winner,))
    c.execute("UPDATE matches set matches = ('%s') WHERE id = ('%s')",(matches,winner,))
    c.execute("SELECT matches FROM matches WHERE id = ('%s')",(loser,))
    matches = c.fetchall()
    matches = matches[0][0] +  1
    c.execute("UPDATE matches set matches = ('%s') WHERE id = ('%s')",(matches,loser,))
    if(winner < loser):
      c.execute("INSERT into history (player1Id, player2Id) VALUES (%s, %s)",(winner, loser,))
    else:
      c.execute("INSERT into history (player1Id, player2Id) VALUES (%s, %s)",(loser, winner,))

    conn.commit()
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
#the user can be paired together provided they do not have a match history stored in the database, nor have they been previously paired
def can_pair(player_pair, rtn):
    player1Id = player_pair[0]
    player2Id = player_pair[2]
    conn = connect()
    c = conn.cursor()
    if(player1Id < player2Id):
      c.execute("SELECT *  FROM history where player1Id = ('%s') and player2Id = ('%s')", (player1Id, player2Id,))
    else:
      c.execute("SELECT *  FROM history where player1Id = ('%s') and player2Id = ('%s')", (player2Id, player1Id,))
    matches = c.fetchall()
    return (matches == [] and player1Id not in rtn and player2Id not in rtn) 

#the swiss pairings will take into account the history of the users, and not match anyone previously paired  
def swissPairings():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, name FROM matches ORDER BY wins DESC")
    to_pair = c.fetchall()
    rtn = []
    history = []
    for each in range(0, len(to_pair) - 1):
        if(can_pair((to_pair[each] + to_pair[each+1]), history)):        
	    rtn.append((to_pair[each] + to_pair[each+1]))
            history.append(to_pair[each][0])
            history.append(to_pair[each + 1][0])
        else:
	  for sub_check in range(each + 1, len(to_pair) -1):
		if(can_pair((to_pair[each] + to_pair[sub_check]), history)):        
		    rtn.append(to_pair[each] + to_pair[sub_check])
                    history.append(to_pair[each][0])
                    history.append(to_pair[sub_check][0])
 
                    break	
    return rtn
    """Returns a list of pairs of players for the next round of a match.

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


