from modules.decoding import *
from modules.container import Container
import random
import copy
import numpy as np

np.random.seed(0)


# -------------------------------------------------------------------------------
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
	
	
def evaluate_solution(container, list_parcels, sequence, cal_fitness=True, balance=False):
	container.reset_container()
	
	# update particle solution to parcels
	for idx, parcel in enumerate(list_parcels):
		parcel.loading_sequence = sequence[idx]
		parcel.change_layout(sequence[idx + len(list_parcels)])
	
	list_parcels = sorted(list_parcels, key=lambda x: x.loading_sequence)
	
	# evaluate fitness value by space utilization
	build_solution(container, list_parcels)
	
	if cal_fitness:
		space_utilization = container.cal_space_ratio()
		balance_ratio, cgx, cgy = container.cal_balance_ratio()
		
		if balance:
			return (1 / 2) * (space_utilization + 10) + (
						1 / 2) * balance_ratio, space_utilization + 10, balance_ratio, cgx, cgy
		else:
			return space_utilization + 10, space_utilization + 10, balance_ratio, cgx, cgy


class Particle:
	def __init__(self, file_index=1, problem_num=1):
		self.pBest_value = None
		self.pBest_sequence = None
		self.fitness_value = None
		self.sequence = None
		self.container = Container(width=233, length=587, height=220, max_weight=35000)
		self.list_parcels = \
			get_list_parcels(file_index=file_index, problem=problem_num, sort_by_base=True)
		
		self.initial_particles()
	
	def initial_particles(self):
		initial_loading_sequence = \
			[i / len(self.list_parcels) for i in range(len(self.list_parcels))]
		initial_layout_sequence: list[None] = [None for _ in range(len(self.list_parcels))]
		
		initial_sequence = initial_loading_sequence + initial_layout_sequence
		
		for idx, parcel_particle in enumerate(self.list_parcels):
			parcel_particle.loading_sequence = initial_sequence[idx]
		
		self.sequence = initial_sequence
		self.fitness_value, self.space_utils, self.balance_ratio, self.cgx, self.cgy = \
			evaluate_solution(self.container, self.list_parcels, self.sequence, balance=True)
		
		self.pBest_sequence = self.sequence
		self.pBest_value = self.fitness_value


class SSO:
	def __init__(self, sso_params, num_gen, num_particles, file_num, prb_no):
		self.gBest_sequence = None
		self.gBest_value = None
		self.gBest_particle = None
		
		self.file_num = file_num
		self.prob_no = prb_no
		
		self.Cg, self.Cp, self.Cw = sso_params[0], sso_params[1], sso_params[2]
		self.num_gen, self.num_particles = num_gen, num_particles
		
		self.list_particles = [Particle(file_num, prb_no) for _ in range(self.num_particles)]
	
	def update_solution(self, particle):
		for idx, val in enumerate(particle.sequence):
			# if (idx in range(30)) or (idx in range(int(len(particle.sequence)/2), int(len(particle.sequence)/2)+30)):
			#     continue
			
			random_number = random.uniform(0, 1)
			
			if random_number < self.Cg:
				particle.sequence[idx] = self.gBest_sequence[idx]
			elif random_number < self.Cp:
				particle.sequence[idx] = particle.pBest_sequence[idx]
			elif random_number < self.Cw:
				continue
			else:
				particle.sequence[idx] = random.uniform(0, 1)
		
		particle.fitness_value, particle.space_utils, particle.balance_ratio, particle.cgx, particle.cgy = \
			evaluate_solution(particle.container, particle.list_parcels, particle.sequence, balance=True)
		
		# update particle pBest fitness value and pBest sequence
		if particle.fitness_value > particle.pBest_value:
			particle.pBest_sequence = particle.sequence
			particle.pBest_value = particle.fitness_value
	
	def update_gBest(self, max_particle):
		self.gBest_particle = copy.copy(max_particle)
		self.gBest_value = self.gBest_particle.pBest_value
		self.gBest_sequence = self.gBest_particle.pBest_sequence
	
	def find_optimal_solution(self):
		list_fitness = []
		
		# initial sequence and calculate fitness value for each particle
		# at the beginning, the loading sequence of parcel follow it orders as base area
		max_particle = max(self.list_particles, key=lambda x: x.pBest_value)
		self.update_gBest(max_particle)
		list_fitness.append(self.gBest_value)
		
		# update sequence of particles
		for idx in range(self.num_gen):
			
			for particle in self.list_particles:
				self.update_solution(particle)
			
			# update gBest
			max_particle = max(self.list_particles, key=lambda x: x.pBest_value)
			
			if max_particle.pBest_value > self.gBest_value:
				self.update_gBest(max_particle)
			
			list_fitness.append(self.gBest_value)
		
		# print(len(max_particle.container.unfitted_parcel), self.gBest_value)
		# print(self.gBest_particle.space_utils, self.gBest_particle.balance_ratio, self.gBest_particle.cgx, self.gBest_particle.cgy)
		
		return self.gBest_particle.container.parcel_inside, \
		       self.gBest_particle.container.container_space, np.array(list_fitness), \
		       len(self.gBest_particle.container.parcel_inside), int(len(self.gBest_sequence) / 2), \
		       self.gBest_particle.balance_ratio, self.gBest_particle.space_utils, \
		       self.gBest_particle.cgx, self.gBest_particle.cgy


def evaluate(num_pop, file_num, prb_num, num_gen, num_particle, sso_param):
	sso_run = {}
	
	pop_dict = {}
	final_list = []
	final_fitted = []
	cgx_list, cgy_list = [], []
	balance_ratio_list = []
	space_utils_list = []
	# plt.figure()
	for pop in range(num_pop):
		sso_alg = SSO(sso_param, num_gen, num_particle, file_num, prb_num)
		optimal_solution, space, list_fitness, fitted, num_parcel, balance_ratio, space_utils, cgx, cgy = \
			sso_alg.find_optimal_solution()
		
		pop_dict[pop] = list_fitness
		final_list.append(list_fitness[-1])
		final_fitted.append(fitted)
		cgx_list.append(cgx)
		cgy_list.append(cgy)
		balance_ratio_list.append(balance_ratio)
		space_utils_list.append(space_utils)
	
	#     plt.plot(list_fitness, label='pop' + str(pop+1))
	
	# plt.xlabel('Generations')
	# plt.ylabel('Space utilization ratio')
	# plt.title(f'Updating results of MOMP-SSO for test instance {prb_num}')
	# plt.grid()
	# plt.legend()
	# plt.ylim((50, 100))
	
	sso_run[sso_param] = pop_dict
	# calculate mean and std
	print(f'mean and std of space utilization {prb_num}: {np.mean(space_utils), np.std(space_utils)}')
	print(f'mean and std of fitted {prb_num}: {np.mean(final_fitted) / num_parcel, np.std(final_fitted) / num_parcel}')
	print(f'mean and std of cgx: {np.mean(cgx_list), np.std(cgx_list)}')
	print(f'mean and std of cgy: {np.mean(cgy_list), np.std(cgy_list)}')
	print(f'mean and std of balance ratio: {np.mean(balance_ratio_list), np.std(balance_ratio_list)}')
	print()
	
	# plt.show()
	return sso_run


# -------------------------------------------------------------------------------
if __name__ == '__main__':
	tools = Tools(233, 587, 220)  # 241, 1353, 269
	
	# create statistics
	sso_param = (0.65, 0.75, 0.85)  # , (0.65, 0.75, 0.85), (0.75, 0.85, 0.90)]
	
	# for prb in [3, 10, 20]:
	#     sso_run = evaluate(10, 1, prb, 30, 5, sso_param)
	
	# sso_run = evaluate(10, 3, 20, 30, 5, sso_param)
	
	# =============================================================================
	
	sso_alg = SSO(sso_param, 1, 10, 1, 3)
	optimal_solution, space, list_fitness, fitted, \
	num_parcel, balance_ratio, space_utils, cgx, cgy \
		= sso_alg.find_optimal_solution()
	
	position, pos_space = [], []
	size, size_space = [], []
	for parcel in optimal_solution:
		position.append(tuple(parcel.position))
		size.append(tuple([parcel.width, parcel.length, parcel.height]))
	
	tools.plot_container(position, size, num_box=len(optimal_solution),
	                     title='Test class 1-3 visualization with merging space')

# for space_ in space:
#     pos_space.append(tuple(space_.start_location))
#     size_space.append(tuple(space_.get_space_dimension()))

# tools.plot_container(pos_space, size_space, num_box=len(space), title='Test class 2-13 visualization of MOMP-SSO result')
# =============================================================================
# plot 140, 30