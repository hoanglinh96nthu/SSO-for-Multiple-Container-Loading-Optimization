from mosso.individual import Individual

class Population:
	def __init__(self, num_inds, container, parcels):
		self.population = [Individual(container, parcels) for _ in range(num_inds)]
		self.pareto_frontier = []