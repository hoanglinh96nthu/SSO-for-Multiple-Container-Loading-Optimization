from mosso.individual import Individual

class Population:
	def __init__(self, num_inds, container, parcels):
		self.population = [Individual(container, parcels) for _ in range(num_inds)]
		self.pareto_frontier = self.find_pareto_frontier()
		self.pop_gBest_value = None
		self.pop_gBest_chromosome = None
		self.calculate_crowding_distance()

	def update_individuals(self):
		pass
	
	def calculate_crowding_distance(self, num_objectives=2):
		for front in self.pareto_frontier:
			if len(front) == 0:
				continue
			
			solutions_num = len(front)
			for individual in front:
				individual.crowding_distance = 0
			
			for m in range(num_objectives):
				front.sort(key=lambda x: x.fitness_value[m])
				front[0].crowding_distance = 10 ** 9
				front[solutions_num - 1].crowding_distance = 10 ** 9
				m_values = [individual.objectives[m] for individual in front]
				scale = max(m_values) - min(m_values)
				if scale == 0: scale = 1
				
				for i in range(1, solutions_num - 1):
					front[i].crowding_distance += \
						(front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale

	def find_pareto_frontier(self):
		"""Return dominated particles"""
		fronts = [[]]

		for individual in self.population:
			individual.domination_count = 0
			individual.dominated_solutions = []

			for other_individual in self.population:

				if individual.dominates(other_individual):
					individual.dominated_solutions.append(other_individual)
				elif other_individual.dominates(individual):
					individual.domination_count += 1

			if individual.domination_count == 0:
				individual.rank = 0
				fronts[0].append(individual)

		i = 0
		while len(fronts[i]) > 0:
			temp = []
			for individual in fronts[i]:
				for other_individual in individual.dominated_solutions:
					other_individual.domination_count -= 1
					if other_individual.domination_count == 0:
						other_individual.rank = i + 1
						temp.append(other_individual)

			i = i + 1
			fronts.append(temp)

		return fronts
