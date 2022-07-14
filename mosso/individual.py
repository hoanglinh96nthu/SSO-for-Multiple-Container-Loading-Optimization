import numpy as np

from modules.decoding import *
from modules.inputs import Input
from modules.container import Container
from modules.parcel import Parcel


def initial_loading_sequence(num_parcels_ind, random=False):
	"""Parcel could be single parcel or stack of several parcels."""
	if random:
		return list(np.concatenate((np.random.uniform(0, 1, size=num_parcels_ind), \
                              [None for _ in range(num_parcels_ind)])))
            
	return list(np.arange(0, num_parcels_ind) / num_parcels_ind) + \
		   [None for _ in range(num_parcels_ind)]

def reset_parcels(list_parcels):
	for parcel in list_parcels:
		parcel.reset_parcels()

def evaluate_solution(loading_sequence, container_ind, parcels):
	container_ind.reset_container()  # empty all existing parcels inside the container
	reset_parcels(parcels)  # remove all state, loading position of the parcel to the origin

	# assign sequence to parcel and load follow the sequence
	for idx, parcel in enumerate(parcels):
		parcel.loading_sequence = loading_sequence[idx]
		parcel.layout = loading_sequence[idx+len(parcels)]

	# load parcels into container and evaluate for its fitness value
	container_ind = build_solution(container_ind, parcels)
	space_utilization = container_ind.cal_space_ratio()
	loaded_ratio = len(container_ind.parcel_inside) / len(parcels)

	return [space_utilization, loaded_ratio]


class Individual:
	def __init__(self, container_ind, parcels):
		self.chromosome = initial_loading_sequence(len(parcels), random=True)
		self.fitness_value = evaluate_solution(self.chromosome, container_ind, parcels)

		self.pBest_value = self.fitness_value
		self.pBest_chromosome = self.chromosome

		self.domination_count = 0
		self.dominated_solutions = None
		self.crowding_distance = None

	def dominates(self, other_individual):
		and_condition = True
		or_condition = False

		for first, second in zip(self.fitness_value, other_individual.fitness_value):
			and_condition = and_condition and first <= second
			or_condition = or_condition or first < second

		return and_condition and or_condition
