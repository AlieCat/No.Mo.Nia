#!/usr/bin/python

from point import *
import math



class angles():
	def __init__(self,point0):
		self.point0=point0
		if (point0.gety()**2+point0.getz()**2)!=0:
			self.radians=math.atan(abs(point0.getx())/math.sqrt(point0.gety()**2+point0.getz()**2))
	def getRadian(self):
		print r
		return self.radians
	def getDeg(self):
		return math.degrees(self.radians)

