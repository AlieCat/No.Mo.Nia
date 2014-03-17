#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import math
import datetime
from point import *
from angle import *
from adxl_control_one import*
from printAngle import *
from funLib import *
#from SaveToWeb import *

# Simple example prints accelerometer data once per second:
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

if __name__ == '__main__':
    
    #creating two objects with the class Adafruit_ADXL345 for the two accelerometer
    accel = Adafruit_ADXL345(0x53)
    accel_patient= Adafruit_ADXL345(0x1D)

    #Is this the first time the program is being run? if so create databases
    DBase =raw_input("Are you running this for the first time? y/n ")
    creating(DBase)

    #set counters, & array sizes
    co=0
    first=0 #know when it's the first iteration
    n=1000 #array length
    myArray=[[0 for j in range(3)] for i in range(n)]#array size
    myArrayPatient=[[0 for j in range(3)] for i in range(n)]#array size
    samplingSize=10 #data used to compute time below 30 and average
    SecondArray= [0]*samplingSize
    SecondArrayPatient= [0]*samplingSize
    name='alie'
    
    #sets the zero point for bed
    raw_input('Put both accelerometers into the zero position then press enter: ')
    c=0 #counter
    while c<(n-1):
	myArray[c]=accel.read()
	myArrayPatient[c]=accel_patient.read()
	c+=1
    if c==(n-1):
	s=avg(myArray)
	p=avg(myArrayPatient)
	c=0
    	print "zero point for Bed: ", s.getx(), s.gety(), s.getz()
	print "zero point for Patient: ", p.getx(), p.gety(), p.getz()
	print " "
	print "Bed Angle is ", angles(s).getDeg()
	print "Patient Angle is ", angles(p).getDeg()
	print " "

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
	n_pt_p=pt_patient.diff(p)
	#puts value in array
	myArrayPatient[c]=n_pt_p

	c=c+1 #adds one to counter

	if (c==(n-1)): #while counter the designated length
		r=avg(myArray) #averages collumns in array
		ang = angles(r)
		deg = ang.getDeg()
		print "Bed angle is ", deg

		pat=avg(myArrayPatient)
		ang_patient = angles(pat)
		deg_patient = ang_patient.getDeg()
		print "Patient angle is ", deg_patient
		
		savingData(ang, ang_patient, name)
		

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
			print "saving results"
		#if co==(samplingSize-1):
			#plotThis(SecondArray,SecondArrayPatient)
			

	elif (c>(n-1)):
		c=0
		co+=1
		print " "
	
		