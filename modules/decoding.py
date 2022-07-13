from inputs import Input
from parcel import Parcel
from modules.container import Container
from tools import Tools
import random


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


def check_fit_space(space, parcel):
	space_dimension = space.get_space_dimension()
	condition = [space_dimension[0] >= parcel.width,
	             space_dimension[1] >= parcel.length,
	             space_dimension[2] >= parcel.height]
	
	if all(condition): return True
	
	return False


def check_exceed_weight(container, parcel):
	weight_inside = container.get_total_parcel_weight()
	if weight_inside + parcel.weight < container.container_max_weight:
		return False
	
	return True


def build_solution(container, list_parcels):
	# initial container space
	container.create_container()
	
	# looping for space in container to load parcels
	for idx, parcel in enumerate(list_parcels):
		can_load = False
		for space in container.container_space:
			
			# check valid space to load parcel
			if check_fit_space(space, parcel) and not check_exceed_weight(container, parcel):
				container.load_parcel(space, parcel)
				can_load = True
				break
		
		if not can_load:
			container.unfitted_parcel.append(parcel)
			parcel.state = 'Doesn\'t fitted'
