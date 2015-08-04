#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

import psycopg2

try:
    conn = psycopg2.connect("")
except:
    print "I am unable to connect to the database"

c = conn.cursor()

def deletePlayers():
  c.execute("DELETE * FROM tournament")
  c.execute("DELETE * FROM matches")
