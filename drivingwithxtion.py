#!/usr/bin/python

'''
This is a term project of Mechatronic Design course in METU mechanical engineering
The aim was achieving a usefull obstacle avoidance application for our four wheeled platform
Below code is prepared for testing the ultrasonic sensors
'''
author = ' BroBots '

import serial
from openni import *



class obsavoid(object):
	
	def __init__(self,x=1):
		self.serMotor = serial.Serial('/dev/ttyACM0',115200)
		#self.f=open('turnxtion.txt','w') 
		self.sat=x  #this is a saturation value, default value is 1, it is recomended that start with smaller x values to avoid large resultant velocities
		self.ctx = Context()
		self.ctx.init()

		# Create a depth generator
		self.depth = DepthGenerator()
		self.depth.create(self.ctx)
		# Set it to VGA maps at 30 FPS
		self.depth.set_resolution_preset(RES_VGA)
		self.depth.fps = 30
		# Start generating
		self.ctx.start_generating_all()
		


	def xtion(self):


		#This function read the measurements from the xtion and return as points_depth

		# Update to next frame
		nRetVal = self.ctx.wait_one_update_all(self.depth)
		self.dmap = self.depth.map  #map of the distances, pixel by pixel
		x=640  #width of the image
		y=480  #height of the image
		
		middle_point = x/2
		points = []
		points_depth = []

		for i in range(-2,3):  #5 nodes are selected from the middle axis
			points.append((middle_point + 105*(i),(y/2)))  #coordinate of the selected points
			n=self.neigh(points[i+2])  #take neighbours of the points to get better measurement
			d=self.pixel2distance(n)  #take the corresponding distance values of the points and neighbours from the depth map
			avg=self.average_distance(d)  #take average (points and neighbours)
			points_depth.append(avg)
		return points_depth
		

		'''
		###If anyone wants to see the image , below code may help to see the image and calibrate it
		
		frame = np.fromstring(depth.get_raw_depth_map_8(), "uint8").reshape(480, 640)

		depthMap = depth.get_tuple_depth_map()

		cv2.imwrite("/home/brobot/Desktop/image.png", frame)

		cv2.imshow('image',frame)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		'''



	def neigh(self,coordinate):

		#this function takes neighbours of given point

		neighbour = [(coordinate[0]+1,coordinate[1]+1) , (coordinate[0]+1,coordinate[1]) , (coordinate[0]+1,coordinate[1]-1) ,\
		             (coordinate[0],coordinate[1]+1) , coordinate , (coordinate[0]-1,coordinate[1]) , \
		             (coordinate[0]+1,coordinate[1]-1) , (coordinate[0],coordinate[1]-1) , (coordinate[0]-1,coordinate[1]-1)]

		return neighbour

	

	def pixel2distance(self,n):

		#This function takes distance values of the points from depth map matrix

		d=[]#mmler
		for i in n:
			dist=self.dmap[i[0],i[1]]   #for dmap; coordinates are x,y
			d.append(dist)

		return d



	def average_distance(self,neighbour):

		#This function simply takes average of given distances
		
		total = 0
		for i in neighbour:
			total=total+i

		return total/len(neighbour)



	def f_xtion(self,depth):

		#This function is an alghorithm to convert the camera readings to meaningful velocity vectors
		#First, every sensor reading is converted to a magnitude and then, they are summing up to generate vector components i,j 
		
		m=[]
		mround=[]
		k=20 #moment coef

		#print depth

		#convert readings to a magnitude value and store them in list m
		for t in depth:
			d=t/10.0            		#mm to cm 
			if d<=125 and d>0:
				m.append(-0.5+d*0.5/125)

			elif d<=200 and d>125:
				m.append(0)

			elif d<=800 and d>200:
				m.append((0.3/600*d) - 0.3*(200/600))
			elif d>800:
				m.append(0.1)
		
			elif d==0.0:
				m.append(-0.5)

		for i in m:
			mround.append(round(i,2))

		print mround
		#the magnitude values are summed up to get velocity vector components i,j
		sumj=0.0
		sumi=0.0
		for j in mround:
			sumj=sumj+j
		

		#sumj=sumj/5.0*3

		#we need a moment component to get an angular velocity
		
		if abs(depth[1] - depth[3]) > 30 or abs(depth[0] - depth[4]) > 30:
			fs=1-abs(depth[1] - depth[3])/5000.0
			moment1 = (mround[1] - mround[3]) *k *fs
			sumi= sumi + moment1
			fb=1-abs(depth[0] - depth[4])/5000.0
			moment2 = (mround[0] - mround[4]) *k *fb
			sumi= sumi + moment2

		
		#final velocity vector compounds of ,first, angular velocity in the positive ccw direction and ,second, linear velocity in the positive y direction
		v=[sumi,sumj]
	
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
	
		
		strtot='<'+'H'+','+str(self.rpmleft)+','+str(self.rpmright)+'>'
		self.serMotor.write(bytes(strtot))
		print strtot
		#self.f.write(str(self.rpmleft)+','+ str(self.rpmright)+"\n")



	def loop(self,v):

		#This function creates a loop to call all necessary functions
			
		if v[0] !=0  or v[1]!=0:
			
			d=self.xtion()
			
			v_xtion=self.f_xtion(d)
			
			vres=self.vectorsum(v_xtion,v)
			
			self.sendrpm(vres)

		# if GUI sends 0,0 ; it means emergency stop
		else:
			vres=[0,0]
			self.sendrpm(vres)











