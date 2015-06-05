#!usr/bin/env python
'''
This is a term project of Mechatronic Design course in METU mechanical engineering
The aim was achieving a usefull obstacle avoidance application for our four wheeled platform
Below code is prepared for testing the ultrasonic sensors
'''
author = ' BroBots '

import serial
import rospy



class obsavoid(object):
	def __init__(self,x=1):
		self.serMotor = serial.Serial('/dev/ttyACM0',115200) 
		self.serSonar = serial.Serial('/dev/ttyACM1',115200)
		self.sat=x  #this is a saturation value, default value is 1, it is recomended that start with smaller x values to avoid large speed 
		self.rpmleft=1  #assume first movement is in the forward direction
		self.rpmright=1
		self.rate = rospy.Rate(4)  #4hz
		#self.f=open('slalom.txt','w')  #log data in a file
		print "obstacle avoidance class is initiliazed"


	def sendSonar(self):

		#This function sends a command to arduino in order to print the sensor measurements on the serial monitor

		self.serSonar.write('<send>')
		self.rate.sleep()



	def sonar(self):
		
		#This function reads the measurements from the ultrasonics and store them in a list as 'cm'

		self.cm=[]
		try:
			a = self.serSonar.readline()

			a=a.split(',')
		
			for i in a:
				try:
					b=int(i)

					self.cm.append(b)
				except:
					self.cm.append(150)
					
		except:
			for i in range(10):
				self.cm.append(150)

		if len(self.cm) < 10:
			for i in range(10-len(self.cm)):
				self.cm.append(150)	


	
	
	def f_ultrasonic(self,v):

		#This function is an alghorithm to convert the sensor readings to meaningful velocity vectors
		#First, every sensor reading is converted to a magnitude and then, they are summing up to generate vector components i,j 

		m=[]
		k=20  #moment coef
		h=20  #angular velocity coef
		
		#the direction is checked to convert corresponding sensor readings
		#other readings in the opposite side are directly equate to 100 to get 0 at the end

		if self.rpmleft < 0 and self.rpmright < 0:   
			self.cmp=[self.cm[0],self.cm[1],self.cm[2],self.cm[3],100,100,100,100,100,self.cm[9]]
		elif self.rpmleft > 0 and self.rpmright > 0:
			self.cmp=[100,100,100,100,self.cm[4],self.cm[5],self.cm[6],self.cm[7],self.cm[8],100]
		else:
			self.cmp = self.cm

		#convert readings to a magnitude value and store them in list m

		for d in self.cmp:
			
			if d<=125 and d>0:
				m.append(-0.5+d*0.5/125)

			elif d<=200 and d>125:
				m.append(0)

			elif d<=800 and d>200:
				m.append((0.3/600*d) - 0.3*(200/600))
			
		
			elif d==0.0:
				m.append(-0.1)

		#By considering the direction of the sensors, the magnitude values are summed up to get velocity vector components i,j

		sumj=0.0  # i is corresponding to angular velocity
		sumi=0.0  # j is corresponding to linear velocity
		
		for j in m[:3]:  #first three sensors are in the back, therefore they create a vector in negative direction for linear velocity
			sumj=sumj-j
		for i in m[3:5]:  #next two are in the left side, therefore they create a vector in ccw direction for angular velocity
			sumi=sumi+i*h
		for j in m[5:8]:  #following three are in the front, therefore they create a vector in positive direction for linear velocity
			sumj=sumj+j
		for i in m[8:]:  #last two are in the right side, therefore they create a vector in cw direction for angular velocity
			sumi=sumi-i*h

		#we need a moment component to get an angular velocity from the front and the back side sensors

		if abs(self.cmp[5] - self.cmp[7]) > 3:
			ff=1-abs(self.cmp[5] - self.cmp[7])/100.0   #function for managing with angled obstacles
			moment1 = (m[5] - m[7]) *k *ff
			sumi= sumi + moment1
			
			fb=1-abs(self.cmp[0] - self.cmp[2])/100.0
			moment2 = (self.cmp[0] - self.cmp[2]) *k *fb
			sumi= sumi + moment2
			#print moment1
		
		v=[sumi,sumj]  #final velocity vector compound of first angular velocity in the positive ccw direction and \
		                                                 #second linear velocity in the positive y direction
		return v


	def vectorsum(self,v1,v2):
		
		#we need to sum velocity vector from GUI and velocity vector from sensors

		xsum=v1[0]+(v2[0]*0.8)
		ysum=v1[1]+(v2[1]*0.8)
		vres=[xsum,ysum]

		self.f.write(str(xsum)+','+ str(ysum)+"\n")

		return vres


	def sendrpm(self,res):
		
		#This function sends final summed up velocity to arduino converting rpm
		
		self.rpmleft=(res[1]-res[0])*45*self.sat 
		self.rpmright=(res[1]+res[0])*45*self.sat		
		
		#regulate meaningless velocity values

		if abs(self.rpmleft) < 10:
			if self.rpmleft<0:
				self.rpmleft=-10
			elif self.rpmleft>0:
				self.rpmleft=10

		if abs(self.rpmright) < 10:
			if self.rpmright<0:
				self.rpmright=-10
			elif self.rpmright>0:
				self.rpmright=10

		if abs(self.rpmleft) > 100:
			if self.rpmleft<0:
				self.rpmleft=-100
			elif self.rpmleft>0:
				self.rpmleft=100

		if abs(self.rpmright) > 100:
			if self.rpmright<0:
				self.rpmright=-100
			elif self.rpmright>0:
				self.rpmright=10				

		strtot='<'+'BroBots'+','+str(self.rpmleft)+','+str(self.rpmright)+'>'

		self.serMotor.write(bytes(strtot))
		print strtot
		
		

	def loop(self,v):

		#This function creates a loop to call all necessary functions
			
		if v[0] !=0  or v[1]!=0:
			
			self.sendSonar()

			cm=self.sonar()
		
			v_sonar=self.f_ultrasonic(v)
			
			vres=self.vectorsum(v_sonar,v)
			
			self.sendrpm(vres)
			
		# if GUI sends 0,0 ; it means emergency stop
		else:  
			vres=[0,0]
			self.sendrpm(vres)