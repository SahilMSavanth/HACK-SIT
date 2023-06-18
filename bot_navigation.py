####### Waste Management System ######



#Importing the required modules 
#############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
###############################################################

###### Defining the functions required ######

###########################################################

# Function for moving forward 
def move_forward(sim):
	left_joint=sim.getObject('/left_joint')
	right_joint=sim.getObject('/right_joint')
	sim.setJointTargetVelocity(left_joint,1)
	sim.setJointTargetVelocity(right_joint,1)
	
#  Function for turning right 
def turn_right(sim):
	left_joint=sim.getObject('/left_joint')
	right_joint=sim.getObject('/right_joint')
	sim.setJointTargetVelocity(left_joint,-0.5)
	sim.setJointTargetVelocity(right_joint,0.5)
	
#  Function for turning left 
def turn_left(sim):
	left_joint=sim.getObject('/left_joint')
	right_joint=sim.getObject('/right_joint')
	sim.setJointTargetVelocity(left_joint,0.5)
	sim.setJointTargetVelocity(right_joint,-0.5)
	
#  Function to stop the bot 
def stop(sim):
	left_joint=sim.getObject('/left_joint')
	right_joint=sim.getObject('/right_joint')
	sim.setJointTargetVelocity(left_joint,0)
	sim.setJointTargetVelocity(right_joint,0)

###########################################################################	
def control_logic(sim):
	
	left_joint=sim.getObject('/left_joint')
	right_joint=sim.getObject('/right_joint')
	turn_count=0
	sim.setJointTargetVelocity(left_joint,0)
	sim.setJointTargetVelocity(right_joint,0)
	white=np.array([255,255,255])
	gray=np.array([154,154,154])
	
    # Initializing the vision sensor for line following and image processing
	while True:
		sensor_handle=sim.getObject("/vision_sensor")
		img,x,y=sim.getVisionSensorCharImage(sensor_handle)
		img=np.frombuffer(img,dtype=np.uint8).reshape(y,x,3)
		img = cv2.flip(cv2.cvtColor(img,cv2.COLOR_BGR2RGB),0)
		
		hsv_img=cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
		upper_hsv=np.array([180,255,255])
		lower_hsv=np.array([0,50,10])
		mask=cv2.inRange(hsv_img,lower_hsv,upper_hsv)


		kernel=np.ones((7,7),np.uint8)
		mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
		mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)

		segment_img=cv2.bitwise_and(img,img,mask=mask)
		contour,_=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		left=img[100,64]
		right=img[100,448]
		
		# Navigating the bot around the arena 
		move_forward(sim)
		
		if np.array_equal(left,white) and np.array_equal(right,gray):
			
				sim.setJointTargetVelocity(left_joint,1)
				sim.setJointTargetVelocity(right_joint,0.5)
				
		if np.array_equal(right,white) and np.array_equal(left,gray):
				sim.setJointTargetVelocity(left_joint,0.5)
				sim.setJointTargetVelocity(right_joint,1)
				
##############################################################################################

################## Main part of the code ######################

if _name_ == "_main_":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:
		# Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()
			
        # Robot navigation using path planning and line following algorithm
		try:
			control_logic(sim)
			time.sleep(5)
			

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		# Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()
