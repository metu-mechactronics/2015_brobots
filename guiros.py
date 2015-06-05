#!/usr/bin/python
'''
This node is build to create a GUI called Virtual Joystick
'''

import rospy
from std_msgs.msg import String
import virtual_joystick_ROS as v 
import threading

class GuiNode(object):

	#This node initialize the GUI and publish velocity vector from it in v_GUI topic

	def __init__(self):
		rospy.init_node('gui',anonymous=True)
		self.rate = rospy.Rate(5) # 4hz
		self.g=threading.Thread(target=v.main)
		self.g.start()
		self.pub=rospy.Publisher('v_GUI',String,queue_size=1000)

	def Publisher(self):
		while self.g.isAlive():
			self.pub.publish(v.a)
			self.rate.sleep()

if __name__=='__main__':
	x=GuiNode()
	x.Publisher()