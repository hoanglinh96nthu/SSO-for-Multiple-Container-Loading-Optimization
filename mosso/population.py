from mosso.individual import Individual

class Population:
	def __init__(self, num_inds, container, parcels):
		self.population = [Individual(container, parcels) for _ in range(num_inds)]
		self.pareto_frontier = self.find_pareto_frontier()
		self.pop_gBest_value = None
		self.pop_gBest_chromosome = None

	def update_individuals(self):
		pass

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
