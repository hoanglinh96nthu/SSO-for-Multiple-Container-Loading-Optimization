import numpy as np
from mosso.population import Population

np.random.seed(1)

class MultiObj_MultiPop_SSO:
    def __init__(self, container, data, num_pops=5, num_gens=50, num_individuals=10):
        self.num_generations = num_gens
        self.num_individuals = num_individuals
        self.num_pops = num_pops
        
        self.container = container
        self.parcel_info = data
        self.total_parcels = len(data)
        self.population = [Population(self.num_individuals, self.container, self.parcel_info) 
                           for _ in range(num_pops)]
    
    def find_optimal_solution(self):
       
        for run in range(self.num_generations):
            pass

        return self.container

    def update_population(self):
        for pop in self.population:
            pop.update_individuals()


        