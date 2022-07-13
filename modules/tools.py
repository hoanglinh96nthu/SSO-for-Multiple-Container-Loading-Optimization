import random as rand
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import matplotlib.pyplot as plt


class Tools:
	def __init__(self, con_length, con_width, con_height):
		"""Containing necessary functions.

		- con_length, con_width, con_height: dimension of the container
		"""
		self.LENGTH = con_length
		self.WIDTH = con_width
		self.HEIGHT = con_height
	
	def plot_container(self, position, size, num_box, title):
		"""Plot box loaded in container as optimized sequences.

		- position: positions = [(0,0,0)], gốc tọa độ của box
		- sizes = [(4,5,3)] size của
		- num_box: to generate different color for each box
		"""
		
		number_of_colors = num_box
		colors = ["#" + ''.join([rand.choice('0123456789ABCDEF') for j in range(6)]) \
		          for i in range(number_of_colors)]
		
		fig = plt.figure()
		ax = fig.add_subplot(projection='3d')
		ax.set_box_aspect((self.LENGTH, self.WIDTH, self.HEIGHT))
		
		pc = self.plotCube(position, size, colors=colors, edgecolor="k")
		ax.add_collection3d(pc)
		
		ax.set_xlim([0, self.LENGTH])
		ax.set_ylim([0, self.WIDTH])
		ax.set_zlim([0, self.HEIGHT])
		ax.set_title(title)
		
		plt.show()
	
	def cuboid_data(self, o, size=(1, 1, 1)):
		X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
		     [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
		     [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
		     [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
		     [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
		     [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
		X = np.array(X).astype(float)
		for i in range(3):
			X[:, :, i] *= size[i]
		X += np.array(o)
		
		return X
	
	def plotCube(self, positions, sizes=None, colors=None, **kwargs):
		if not isinstance(colors, (list, np.ndarray)):
			colors = ["C0"] * len(positions)
		if not isinstance(sizes, (list, np.ndarray)):
			sizes = [(1, 1, 1)] * len(positions)
		
		g = []
		for p, s, c in zip(positions, sizes, colors):
			g.append(self.cuboid_data(o=p, size=s))
		
		return Poly3DCollection(np.concatenate(g), edgecolors='k',
		                        facecolors=np.repeat(colors, 6),
		                        linewidths=1, alpha=0.8, **kwargs)
	
	def plot_graph(self, y_line, lable):
		"""
		Plot graph.

		- x_line, y_line: data for plot 2d graph (x=[1, 2, 3,...], y = [2, 6, 0,...])
		- lable for x_line and y_line: list([x axis, y_axis, lable_line, lable_graph])
		"""
		y = y_line.tolist()  # convert numpy array to list
		x_line = [i for i in range(len(y))]
		plt.plot(x_line, y, label=lable[2])
		plt.xlabel(lable[0])  # naming the x axis
		plt.ylabel(lable[1])  # naming the y axis
		plt.title(lable[3])  # giving a title to my graph
		plt.legend()  # show a legend on the plot
		plt.show()  # function to show the plot

# Reference: https://stackoverflow.com/questions/49277753/python-matplotlib-plotting-cuboids