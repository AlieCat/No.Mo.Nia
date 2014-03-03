#!/usr/bin/python

class point(object):
	def __init__(self,x,y,z):
		self.x=x
		self.y=y
		self.z=z
	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getz(self):
		return self.z
	def diff(self, point1):
		newpoint=point(abs(self.x-point1.getx()),abs(self.y),abs(self.z))
		return newpoint




		