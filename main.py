import matplotlib.pyplot as plt
import numpy as np

from modules.container import Container
from modules.inputs import Input as read_data
from modules.parcel import Parcel
from modules.tools import Tools
from mosso.mosso import MultiObj_MultiPop_SSO


def get_list_parcels(file_index=1, problem=1):
    input_data = read_data(file_number=file_index, problem_number=problem)
    # use raw data file as input
    
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
    
    return parcel_lists

def visualize_loading_solution(solution, info):
    container_width, container_length, container_height = \
        info['container_dimension'][:]
    tools = Tools(container_width, container_length, container_height)

    position, pos_space = [], []
    size, size_space = [], []
    for parcel in solution:
        position.append(tuple(parcel.position))
        size.append(tuple([parcel.width, parcel.length, parcel.height]))

    tools.plot_container(position, size, num_box=len(solution))


if __name__ == '__main__':
    file_num, problem_num = 1, 1
    data = get_list_parcels(file_num, problem_num)
    container = Container(width=233, length=587, height=220, max_weight=35000)
    
    model = MultiObj_MultiPop_SSO(container, data, num_pops=1, num_gens=50, num_individuals=100)
    optimal_solution = model.find_optimal_solution()
    
    # show pareto frontier of a solution
    frontier = []
    for ind in model.population[0].population:
        frontier.append(ind.fitness_value + [ind.rank])
        
    frontier = np.array(frontier)
    plt.scatter(x=frontier[:, 0], y=frontier[:, 1], c=frontier[:, 2])
    plt.show()
    
    # visualize optimal solution
    # sol_info = {'container_dimension': [241, 587, 269]}
    # sol_info = {
    #     'container_dimension': [241, 1353, 269],
    #     'space_utilization': optimal_solution.space_utilization,
    #     'balance_ratio': optimal_solution.balance_ratio,
    #     'loaded_ratio': [optimal_solution.loaded_parcels, optimal_solution.total_parcels]
    # }
    # visualize_loading_solution(optimal_solution.parcel_inside, info=sol_info)
