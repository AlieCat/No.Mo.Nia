#!/usr/bin/python

from point import *
#from bigfloat import*
import math



class angles():
	def __init__(self,point0):
		self.point0=point0
		self.x=abs(float(point0.getx()))
		self.y=math.sqrt((float(point0.gety()**2+point0.getz()**2)))
		self.radians=math.atan2(self.x,self.y)
	def getRadian(self):
		return self.radians
	def getDeg(self):
		return math.degrees(self.radians)

