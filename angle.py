#!/usr/bin/python

from point import *
import math



class angle():
	def __init__(self,point0):
		self.point0=point0
		diffpoint=point0
		if (diffpoint.gety()**2+diffpoint.getz()**2)!=0:
			self.radians=math.atan(diffpoint.getx()/math.sqrt(diffpoint.gety()**2+diffpoint.getz()**2))
		#elif (diffpoint.getz()**2+diffpoint.getx()**2)!=0:
		#	self.radians=math.atan(diffpoint.gety()/math.sqrt(diffpoint.getz()**2+diffpoint.getx()**2))
		#else:
		#	self.radians=0
	def getRadian(self):
		return self.radians
	def getDeg(self):
		return math.degrees(self.radians)

