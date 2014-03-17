#!/usr/bin/python

import math
import datetime
import time
import sqlite3 as lite
import sys

def creating(first):
    if first=="y":
    	con=lite.connect('patient1.db')
    	with con:
        	cur =con.cursor()
		cur.execute("CREATE TABLE Data(DateTime REAL, Angle REAL, PatientAngle REAL)")
		cur.execute("CREATE TABLE Results(DateTime REAL, Average REAL, TimeBelow30 INT)")
	created=True
    else:
	created=False
    return created

def savingData(deg, pdeg, patientname):
    con=lite.connect('patient1.db')
    with con:
        cur =con.cursor()
	#cur.execute("CREATE TABLE Data(DateTime REAL, Angle REAL, PatientAngle REAL)")
	when=time.time()
	cur.execute("INSERT INTO Data VALUES(?, ?, ?)", (when, deg.getDeg(), pdeg.getDeg()))
    save=True
    return save

def savingValues(deg, filename):
    when=datetime.datetime.now()
    when=str(when)
    target=open(filename, 'a')
    target.write(when)
    target.write("	")
    deg=str(deg)
    target.write(deg)
    target.write("\n")
    save=True
    return save

def savingResults(tBelo, Avg, s):
    when=datetime.datetime.now()
    when=str(when)
    target=open("results.txt", 'a')
    target.write(when)
    target.write(" ")
    target.write("Time Below 30 degrees was ")
    tBelo=str(tBelo)
    target.write(tBelo)
    target.write(" Average angle was ")
    Avg=str(Avg)
    target.write(Avg)
    target.write(s)
    target.write("\n")
    #print "Saving"
    save=True
    return save
