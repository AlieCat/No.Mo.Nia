#library of functions
import math
#import numpy
from pylab import *
from point import*
from adxl_control_one import *


def timeBelo(Array):
	c=0
	Belo=0
	max=len(Array)
	while(c<max):
		if (Array[c]<30):
			Belo+=1
		c+=1
	return Belo

def aver(Array):
	max=len(Array)
	summa=sum(Array)
	#print "calculating avg----"
	avf=summa/max
	#print avf
	return avf

#Average X,Y, and Z coordinates outputed from the accelerometer
#finds the average of collumns in an array
#Note this is not a true average 
#because both numbers are considered integers and the remainder is discarded
def avg(array):
	sumx=0
	sumy=0
	sumz=0
	for x in range (0,len(array)-1):
		sumx+=array[x].getx()
		sumy+=array[x].gety()
		sumz+=array[x].getz()
	avgX=sumx/len(array)
	avgY=sumy/len(array)
	avgZ=sumz/len(array)
	average=point(avgX,avgY,avgZ)
	return average


def compare(degB, degP, diff):
	if (degP<degB and (degB-degP)>diff):
		k=" patient may be slipping"
	#elif ((degB-degP)>diff and degB<30):
	#	k=" patient is slipping below 30 degrees"
	else:
		k=" "
	return k

def plotThis(degB, degP):
	timeAxis=[0,1,2,3,4,5,6,7,8,9]
	figure()
	plot(timeAxis, degB, label="bed angle")
	plot(timeAxis, degP, 'g', label="patient angle")
	legend(loc=0)
	xlabel('time')
	ylabel('angle')
	savefig("BedPatientAngle.png")
	close()
	return 0


