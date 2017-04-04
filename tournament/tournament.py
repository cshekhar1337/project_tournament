#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Connection Error")

def execQuery(query):
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    cur.close()



def deleteMatches():
    """Remove all the match records from the database."""
    query = "delete from matches"
    execQuery(query)

def deletePlayers():
    """Remove all the player records from the database."""
    
    query = "delete from players"
    execQuery(query)
   

def countPlayers():
    """Returns the number of players currently registered."""
    con = connect()
    
    query = "select COALESCE(count(name),0) from players"

    cur = con.cursor()
    cur.execute(query)
    val = cur.fetchone()
    con.commit()
    cur.close()
    return val[0]



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    con = connect()
    query = "INSERT INTO players (name) VALUES (%s)"
    val = (name ,)
    cur = con.cursor()
    cur.execute(query,val)
    con.commit()
    cur.close()



def playerStandings():
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
    con = connect()
    # join query on the two tables to get standing of each player. Used joins and aggregate function to get wins.

    query1 = '''
    select t5.id, t5.name, COALESCE(t4.win_count, 0) as wins, COALESCE(t4.tot, 0) as total_matches  from 
    ((SELECT id1, count(id1) as win_count from matches group by id1 ) as t1
    RIGHT JOIN 
    (select id, count(id) as tot from players, matches where id = id1 or id = id2 group by id) as t2
    on t2.id = t1.id1) as t4
    RIGHT JOIN 
    (select id, name from players) as t5 
    on t5.id = t4.id  or t4.id IS NULL 
    order by wins DESC;
    '''
    
    cur = con.cursor()
    #print(cur.mogrify(query1))
    cur.execute(query1)
    con.commit()
    resList = cur.fetchall()
    cur.close()
    return resList

    

    


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    con = connect()
    
    query1 = "INSERT INTO matches (id1, id2) VALUES (%s , %s)"
    val1 = (winner , loser)
    cur = con.cursor()
    cur.execute(query1, val1)
    con.commit()
    cur.close()
    """
    query2 = "UPDATE players SET no_matches = no_matches + 1 where id = %s or id = %s " # query to update players table to modify no of matches the player has played
    val2 = (winner, loser)
    cur = con.cursor()
    #print(cur.mogrify(query2,val2))
    cur.execute(query2, val2)
    con.commit()
    cur.close()
    """



def swissPairings():
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

    standings = playerStandings() # use standing to get player standing in current round
    result = []
    i = 0
    
    while i < len(standings):
# player1, player2 are grouped together as win_count is in the descending order. so players with winning equal or close are adjacent in the list
        player1_details, player2_details = standings[i], standings[i+1] 
        i+= 2
       
        player1_id , player1_name = player1_details[0], player1_details[1]
        player2_id, player2_name = player2_details[0], player2_details[1]
       
        result.append((player1_id, player1_name, player2_id, player2_name))
    return result

        








