import numpy as np
from mosso.population import Population

np.random.seed(1)

class MultiObjectiveSSO:
    def __init__(self, container, data, num_pops=5, num_gens=50, num_individuals=10):
        self.num_generations = num_gens
        self.num_individuals = num_individuals
        self.num_pops = num_pops
        
        self.population = None
        self.container = container
        self.parcel_info = data
        self.total_parcels = len(data)
    
    def find_optimal_solution(self):
        self.create_population(self.num_pops, self.num_individuals, self.container, self.parcel_info)
        
        for run in range(self.num_generations):
            pass

    def create_population(self, num_pops, num_individuals, container, parcels):
        self.population = [Population(num_individuals, container, parcels) for _ in range(num_pops)]
        
        # find pareto frontier for initial population


        