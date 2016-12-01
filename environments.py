import simObjects
import math
class Environment(object):
	def __init__(self, init_objects = []):
		for env_object in init_objects:
			self.env_objects.append(env_object)

	def Add_Env_Object(env_object):
		self.env_objects.append(env_object)

	def Add_Env_Object_List(env_objects):
		for env_object in env_objects:
			self.env_objects.append(env_object)

	def Send_To_Simulator(self, sim, ID_offset):
		for env_object in self.env_objects:
			env_object.Send_To_Simulator(sim,ID_offset=ID_offset)
			ID_offset += 1


class Sym_Env(Environment):
 	"""docstring for Tree_E"""
 	def __init__(self, num_objects, radius, distance, num_groups=2, origin=(0.,1.,0.5)):
 		super(Sym_Env,self).__init__()
	 	self.joints = []
	 	self.group_centers = [0]*num_groups
	 	self.group_orthagonal = [0]*num_groups

	 	center_angle = math.pi/2.0

	 	incr = 1.0/float(num_groups+2.0)
	 	mult = 1
	 	for i in range(0,num_groups,2):
	 		pos_angle = center_angle+mult*incr
	 		neg_angle = center_angle-mult*incr
	 		self.group_centers[i] = [math.cos(pos_angle),math.sin(pos_angle),origin[2]]
	 		self.group_orthagonal[i] = [ math.sin(neg_angle), math.cos(neg_angle), 0]
	 		self.group_centers[i+1] = [math.cos(neg_angle),math.sin(neg_angle),origin[2]]
	 		self.group_orthagonal[i+1] = [ math.sin(pos_angle), math.cos(neg_angle), 0]
	 		mult += 1

 		for i in range(num_groups):
 			for j in range(2):
 				self.group_centers[i][j] = self.group_centers[i][j]*distance+origin[j]

if __name__=="__main__":
 	env = Sym_Env(2,1,1)
 	print env.group_centers
 	print env.group_orthagonal

 	import matplotlib.pyplot as plt

 	plt.plot([0, env.group_centers[0][0], env.group_centers[0][0]+env.group_orthagonal[0][0]],
 				[1,env.group_centers[0][1], env.group_centers[0][1]+env.group_orthagonal[0][1]])
 	plt.plot([0, env.group_centers[1][0]],[1,env.group_centers[1][1]])
 	plt.show()