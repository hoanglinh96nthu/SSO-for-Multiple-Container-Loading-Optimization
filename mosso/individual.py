import numpy as np
from modules.decoding import *
from modules.inputs import Input
from modules.container import Container
from modules.parcel import Parcel


def initial_loading_sequence(num_parcels):
	"""Parcel could be single parcel or stack of several parcels"""
	return list(np.arange(0, num_parcels)/num_parcels) + [None for _ in range(num_parcels)]

def reset_parcels(list_parcels):
	for parcel in list_parcels:  parcel.reset_parcels()

def evaluate_solution(loading_sequence, container, parcels):
	container.reset_container()  # empty all existing parcels inside the container
	reset_parcels(parcels)  # remove all state, loading position of the parcel to the origin
	
	# assign sequence to parcel and load follow the sequence
	for idx, parcel in enumerate(parcels):
		parcel.loading_sequence = loading_sequence[idx]
		parcel.layout = loading_sequence[idx+len(parcels)]
		
	# load parcels into container and evaluate for its fitness value
	container = build_solution(container, parcels)
	space_utilization = container.cal_space_ratio()
	loaded_ratio = len(container.parcel_inside) / len(parcels)
	
	return [space_utilization, loaded_ratio]


def get_list_parcels(file_index=1, problem=1, sort_by_base=True):
	input_data = Input(file_number=file_index, problem_number=problem)  # use raw data file as input
	
	# load parcel information from data
	parcel_lists = []
	
	for box_type in range(input_data.ntype):
		for num_box in range(int(input_data.boxes[box_type, 6])):
			length = input_data.boxes[box_type, 2]
			width = input_data.boxes[box_type, 0]
			height = input_data.boxes[box_type, 4]
			
			weight = input_data.boxes[box_type, 7]
			
			rotate = [int(input_data.boxes[box_type, 1]),
			          int(input_data.boxes[box_type, 3]),
			          int(input_data.boxes[box_type, 5])]
			
			new_parcel = Parcel(box_type, width, length, height, weight, rotate)
			
			# create info list of parcel
			parcel_lists.append(new_parcel)
	
	if sort_by_base:
		return sorted(parcel_lists, key=lambda x: x.base_area, reverse=True)
	else:
		for parcel in parcel_lists:
			parcel.loading_sequence = random.uniform(0, 1)
		
		return sorted(parcel_lists, key=lambda x: x.loading_sequence)
	
	
class Individual:
	def __init__(self, container, parcels):
		self.chromosome = initial_loading_sequence(len(parcels))
		self.fitness_value = evaluate_solution(self.chromosome, container, parcels)
		
		self.pBest_value = self.chromosome
		self.pBest_chromosome = self.fitness_value


if __name__ == '__main__':
	data = get_list_parcels()
	num_parcels = len(data)
	container = Container(width=233, length=587, height=220, max_weight=35000)
	
	indi = Individual(container, data)
	chromosome = initial_loading_sequence(num_parcels)
	fitness = evaluate_solution(chromosome, container, data)
	print(fitness)