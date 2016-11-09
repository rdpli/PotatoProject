import math
import copy

class Tree(object):
	def __init__(self,num_children=2,current_depth=0,max_depth=2,base_position=[0,0,0],
					branch_length=1,global_angle=0,lo_angle=-math.pi/4,hi_angle= math.pi/4,node_ID=0,parent_ID=None):

		print node_ID, num_children

		self.node_ID = node_ID
		self.parent_ID = parent_ID
		self.highest_child_ID = node_ID
		self.branch_length = branch_length

		self.base_position = base_position
		self.tip_position = [0]*3
		self.tip_position[0] = base_position[0] +  self.branch_length*math.cos(global_angle)

		self.tip_position[1] = base_position[1] +  self.branch_length*math.sin(global_angle)
		self.tip_position[2] = base_position[2]


		self.depth = current_depth
		self.max_depth = max_depth

		self.angle = global_angle


		self.is_leaf = False
		if self.depth == max_depth:
			self.is_leaf = True
			self.children = []
			self.num_children = 0
		else:
			if isinstance(num_children,int):
				self.num_children = num_children
				self.lineage = num_children
			else:
				self.num_children = num_children[0]
				self.lineage = [0]*(len(num_children)-1)
				for i in range(len(self.lineage)):
					self.lineage[i] = num_children[i+1]

			self.children = []
			angle_incr = (hi_angle- lo_angle)/ float(self.num_children-1)

			for nc in range(self.num_children):
				child_angle = self.angle + lo_angle + nc*angle_incr
				child_ID = self.highest_child_ID + 1
				child = Tree(num_children=self.lineage, current_depth=self.depth+1,
					max_depth=self.max_depth, base_position=self.tip_position, branch_length=self.branch_length,
					global_angle=child_angle,lo_angle=lo_angle/2.0,hi_angle=hi_angle/2.0, 
					node_ID=child_ID,parent_ID=self.node_ID)
				self.children.append(child)
				self.highest_child_ID = self.children[-1].highest_child_ID


	def Plot_Tree(self,ax):
		plt.plot([self.tip_position[0],self.base_position[0]],[self.tip_position[1],self.base_position[1]])
		center = self.Get_Center()
		ax.text(center[0],center[1],str(self.node_ID))
		for c in self.children:
			c.Plot_Tree(plt)

	def Get_Center(self):
		center = [0]*3
		for i in range(3):
			center[i] = (self.base_position[i]+self.tip_position[i])/2.0
		return center


if __name__ == "__main__":
	import matplotlib.pyplot as plt
	num_children = 4
	max_depth = 2
	branch_length = .75


	t = Tree(num_children=num_children,current_depth=0,max_depth=max_depth, 
		branch_length=branch_length,
		base_position=[0,0,0.5],lo_angle=-math.pi/4.,hi_angle=math.pi/4.,global_angle=math.pi/2.0,node_ID=0)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	t.Plot_Tree(ax)
	plt.show()
