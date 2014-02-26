import math
import datetime

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
