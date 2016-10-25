import networks
from pyrosim import PYROSIM
import math

class Quadruped():
	

	def __init__(self,x=0,y=0,z=0.3,body_length=0.5,body_height=0.1,objID=0,jointID=0,sensorID=0,color=[0,0,0],network=-1,z_incr=0.05): 
		self.pos = self.x,self.y,self.z = x,y,z
		self.body_length = body_length
		self.body_height = body_height
		self.color = self.r,self.g,self.b = color
		self.network = network
		self.z_incr = z_incr
		self.leg_length = self.z
		self.radius = .5*self.body_height


	def Add_Network(self,network):
		self.network = network

	def Send_To_Simulator(self,sim, objID=0,jointID=0,sensorID=0,neuronID=0,send_network=True):
		
		init_sensorID = sensorID
		init_jointID = jointID
		init_objID = objID
		#self.Send_Body()

		bodyID = objID
		objID += 1
		(r,g,b) = self.color

		#Body 
		sim.Send_Box(ID=bodyID, x=self.x,y=self.y,z=self.z+self.z_incr,
					length=self.body_length,width=self.body_length,
					height=self.body_height,r=self.r,g=self.g,b=self.b)

		#Auto asign legs based on how high the body is set to be

		delta = 0.
		for i in range(4):
			leg_x = math.cos(delta)
			leg_y = math.sin(delta)
			delta += math.pi/2.0
			bl_length1 = (self.body_length+self.leg_length)/2.
			bl_length2 = self.body_length/2.+self.leg_length

			thighID = objID
			objID += 1
			calfID = objID
			objID += 1
			#Thigh
			sim.Send_Cylinder(ID=thighID, x=leg_x*bl_length1+self.x,y=leg_y*bl_length1+self.y,
								z=self.z+self.z_incr,r1=leg_x,r2=leg_y,r3=0,length=self.leg_length,
								radius=self.radius,r=self.r,g=self.g,b=self.b)
			
			#Calf
			sim.Send_Cylinder(ID=calfID, x=leg_x*bl_length2+self.x,y=leg_y*bl_length2+self.y,
								z=self.z/2.+self.z_incr,r1=0,r2=0,r3=1, length=self.z,radius=self.radius,
								r=self.r,g=self.g,b=self.b)

			#Hip joint
			sim.Send_Joint(ID=jointID, firstObjectID=bodyID, secondObjectID=thighID, 
							x=leg_x*self.body_length/2.+self.x,y=leg_y*self.body_length/2.+self.y,z=self.z+self.z_incr,
							n1=leg_y,n2=leg_x,n3=0)
			jointID+=1

			#Knee Joint
			sim.Send_Joint(ID=jointID, firstObjectID=thighID, secondObjectID=calfID, 
							x=leg_x*bl_length2+self.x,y=leg_y*bl_length2+self.y,z=self.z+self.z_incr,
							n1=leg_y,n2=leg_x,n3=0)
			jointID+=1

			#Sensor on feet
			sim.Send_Touch_Sensor(ID=sensorID, objectIndex=calfID)
			sensorID += 1
		
		#Send a position sensor attached to the body
		sim.Send_Position_Sensor(ID=sensorID,objectIndex=bodyID)
		sensorID +=1

		last_sensorID = sensorID
		last_objID = objID
		last_jointID = jointID

		##### SEND NETWORK ###############################
		if send_network:

			if self.network == -1:
				self.network = networks.LayeredNetwork()

			#Sends a neural net to the simulator
			sensor_neuron_start = neuronID
			for sensor_index in range(self.network.num_sensors): #Send sensor neurons to sim
				sim.Send_Sensor_Neuron(ID=sensor_neuron_start+sensor_index,sensorID=sensor_index+init_sensorID)

			hidden_neuron_start = sensor_neuron_start + self.network.num_sensors
			for hidden_index in range(self.network.num_layers*self.network.num_hidden): #Send hidden neurons to sim
				sim.Send_Hidden_Neuron(ID=hidden_neuron_start+hidden_index)

			motor_neuron_start = hidden_neuron_start + self.network.num_hidden*self.network.num_layers
			for motor_index in range(self.network.num_motors): #Send motor neurons to sim
				sim.Send_Motor_Neuron(ID=motor_neuron_start+motor_index, jointID= init_jointID+motor_index)

			for i in range(self.network.total_neurons):
				for j in range(self.network.total_neurons):
					if not(self.network.adj_matrix[i,j]==0): #Connect neurons with synapses from network adj matrix
						sim.Send_Synapse( neuronID+i,neuronID+j,self.network.adj_matrix[i,j])

			last_neuronID = neuronID + self.network.total_neurons

		

		if send_network:
			return last_objID,last_jointID,last_sensorID,last_neuronID
		else:
			return last_objID,last_jointID,last_sensorID




if __name__ == "__main__":
	import numpy as np
	T = 1000
	sim = PYROSIM(playPaused=False, playBlind=False, evalTime=T)

	objID = 0
	jointID = 0
	sensorID = 0
	neuronID = 0
	pos_sensor_list = []
	N = 4
	for i in range(N): #Create N potatoes, each with a different random flavor
		color = np.random.rand(3)
		myQuad = Quadruped(x=i*1.5-N/2,color=color)
		objID,jointID,sensorID,neuronID = myQuad.Send_To_Simulator(sim, objID=objID,jointID=jointID,sensorID=sensorID,neuronID=neuronID)
		pos_sensor_list.append(sensorID-1)

	sim.Start()
	sim.Wait_To_Finish()
	print pos_sensor_list
	for i in range(N):
		for j in range(3):
			print sim.Get_Sensor_Data(pos_sensor_list[i],j,T-1)
		print '--------'


