#!/usr/bin/env python
'''
This node is build to control our platform and get feedback from ultrasonic sensors on it
'''

import rospy
from std_msgs.msg import String
import drivingwithultrasonic as d  #change file to xtion
import threading

class ProBot():
	def __init__(self):
		rospy.init_node('ProBot',anonymous = True)
		self.pub = rospy.Publisher('platformfeedback',String,queue_size=1000)	
		self.d=d.obsavoid()
		
	
	def subscribed(self):
		rospy.Subscriber('v_GUI',String,self.velocity)
		rospy.spin()
		
	def velocity(self,data):

		#when a velocity vector comes from GUI, this function parse it and call loop function to calculate velocity vector from sensors

		v_GUI=data.data
		v = v_GUI.split(",")
		v_GUI=[]
		for i in v:
			v_GUI.append(float(i))

		self.d.loop(v_GUI)
		
							
if __name__=='__main__':
	x=ProBot()
	x.subscribed()