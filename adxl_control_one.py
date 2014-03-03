#!/usr/bin/python

# Python library for ADXL345 accelerometer.

# Copyright 2013 Adafruit Industries

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import math
import datetime
from point import *
from angle import *
#from numpy import *




from Adafruit_I2C import Adafruit_I2C

from printAngle import savingValues, savingResults
from funLib import timeBelo, aver, avg, compare, plotThis
#from SaveToWeb import *


class Adafruit_ADXL345(Adafruit_I2C):
    # base class = Adafruit_12C
    # inherited read readU8, write8, readlist

    # Minimal constants carried over from Arduino library



    ADXL345_REG_DEVID        = 0x00 # Device ID
    ADXL345_REG_DATAX0       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
    ADXL345_REG_POWER_CTL    = 0x2D # Power-saving features control

    ADXL345_DATARATE_0_10_HZ = 0x00
    ADXL345_DATARATE_0_20_HZ = 0x01
    ADXL345_DATARATE_0_39_HZ = 0x02
    ADXL345_DATARATE_0_78_HZ = 0x03
    ADXL345_DATARATE_1_56_HZ = 0x04
    ADXL345_DATARATE_3_13_HZ = 0x05
    ADXL345_DATARATE_6_25HZ  = 0x06
    ADXL345_DATARATE_12_5_HZ = 0x07
    ADXL345_DATARATE_25_HZ   = 0x08
    ADXL345_DATARATE_50_HZ   = 0x09
    ADXL345_DATARATE_100_HZ  = 0x0A # (default)
    ADXL345_DATARATE_200_HZ  = 0x0B
    ADXL345_DATARATE_400_HZ  = 0x0C
    ADXL345_DATARATE_800_HZ  = 0x0D
    ADXL345_DATARATE_1600_HZ = 0x0E
    ADXL345_DATARATE_3200_HZ = 0x0F

    ADXL345_RANGE_2_G        = 0x00 # +/-  2g (default)
    ADXL345_RANGE_4_G        = 0x01 # +/-  4g
    ADXL345_RANGE_8_G        = 0x02 # +/-  8g
    ADXL345_RANGE_16_G       = 0x03 # +/- 16g
    def __init__(self, address, busnum=-1, debug=False):
        self.accel = Adafruit_I2C(address, busnum, debug)
        if self.accel.readU8(self.ADXL345_REG_DEVID) == 0xE5:
            # Enable the accelerometer
            self.accel.write8(self.ADXL345_REG_POWER_CTL, 0x08)
	self.origin=point(0,0,0)
    def setRange(self, range):
        # Read the data format register to preserve bits.  Update the data
        # rate, make sure that the FULL-RES bit is enabled for range scaling
        format = ((self.accel.readU8(self.ADXL345_REG_DATA_FORMAT) & ~0x0F) |
          range | 0x08)
        # Write the register back to the IC
        seld.accel.write8(self.ADXL345_REG_DATA_FORMAT, format)
    def getRange(self):
        return self.accel.readU8(self.ADXL345_REG_DATA_FORMAT) & 0x03
    def setDataRate(self, dataRate):
        # Note: The LOW_POWER bits are currently ignored,
        # we always keep the device in 'normal' mode
        self.accel.write8(self.ADXL345_REG_BW_RATE, dataRate & 0x0F)
    def getDataRate(self):
        return self.accel.readU8(self.ADXL345_REG_BW_RATE) & 0x0F
    # Read the accelerometer
    def read(self):
        raw = self.accel.readList(self.ADXL345_REG_DATAX0, 6)
        res = []
        for i in range(0, 6, 2):
            g = raw[i] | (raw[i+1] << 8)
            if g > 32767: g -= 65536
            res.append(g)
        return point(res[0],res[1],res[2])
    def set0(self):
	self.origin=point(self)
	return self.origin
	



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
	
		
	
		



