#!/usr/bin/python

import math
import datetime
from point import *
from angle import *
from adxl_control_one import*

from printAngle import savingValues, savingResults
from funLib import timeBelo, aver, avg, compare, plotThis
#from SaveToWeb import *

# Simple example prints accelerometer data once per second:
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.OUT)

if __name__ == '__main__':
    
    #creating two object with the class Adafruit_ADXL345 for the two accelerometer
    accel = Adafruit_ADXL345(0x53)
    accel_patient= Adafruit_ADXL345(0x1D)

    #set counters, & array sizes
    c=0 #counter
    co=0 #second counter
    first=0 #know when it's the first iteration
    n=1000 #array length
    myArray=[[0 for j in range(3)] for i in range(n)]#array size
    myArrayPatient=[[0 for j in range(3)] for i in range(n)]#array size
    samplingSize=10 #data used to compute time below 30 and average
    SecondArray= [0]*samplingSize
    SecondArrayPatient= [0]*samplingSize
    name="bedAngle.txt"
    
    #sets the zero point (s)
    raw_input('Put both accelerometers into the zero position then press enter: ')
    while c<(n-1):
	myArray[c]=accel.read()
	c+=1
    if c==(n-1):
	s=avg(myArray)
	c=0
    print "zero point: ", s.getx(), s.gety(), s.getz()

    while True:

	#getting the bed angle
	pt = accel.read()
	#calibrating the bed angle
	n_pt=pt.diff(s)
	#puts value in array
	myArray[c]=n_pt

	
	#getting patient
	pt_patient = accel_patient.read()
	#calibrating the patient angle
	
	#puts value in array
	myArrayPatient[c]=pt_patient

	c=c+1 #adds one to counter

	if (c==(n-1)): #while counter the designated length
		r=avg(myArray) #averages collumns in array
		ang = angle(r)
		deg = ang.getDeg()
		print "Bed angle is ", deg

		p=avg(myArrayPatient)
		ang_patient = angle(p)
		deg_patient = ang_patient.getDeg()
		print "Patient angle is ", deg_patient


		savingValues(ang, name) #saves to .txtfile
		savingValues(ang_patient, 'SternumAngleAlie.txt')
		

		if (first==0):
			SecondArray[co]=ang #creates array with lower sampling rate
			SecondArrayPatient[co]=ang_patient
		elif (first==1):
			del SecondArray[0]	#deletes first value in array
			del SecondArrayPatient[0]
			SecondArray.append(ang)
			SecondArrayPatient.append(ang_patient)


																																									
		if (co>=(samplingSize-1)):
			#print "calculating patient risk..."
			tbelo=timeBelo(SecondArray)
			#Avg=aver(SecondArray)
			#slip=compare(ang, ang_patient, initDiff)
			#co=0
			first = 1																																																																		
			#savingResults(tbelo, Avg, slip)
		#if co==(samplingSize-1):
			#plotThis(SecondArray,SecondArrayPatient)
			

	elif (c>(n-1)):
		c=0
		co+=1
		print " "
	
		