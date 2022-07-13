from mosso import MultiObjectiveSSO
from modules.inputs import Input as read_data
from modules.tools import Tools


def visualize_loading_solution(solution, info):
    container_width, container_length, container_height = sol_info['container_dimension'][:]
    tools = Tools(container_width, container_length, container_height)

    position, pos_space = [], []
    size, size_space = [], []
    for parcel in solution:
        position.append(tuple(parcel.position))
        size.append(tuple([parcel.width, parcel.length, parcel.height]))

    tools.plot_container(position, size, num_box=len(optimal_solution))


if __name__ == '__main__':
    file_num, problem_num = 1, 1
    data = read_data(file_num, problem_num)
    
    model = MultiObjectiveSSO()
    optimal_solution = model.find_optimal_solution(data)
    
    # visualize optimal solution
    sol_info = {
        'container_dimension': [241, 1353, 269],
        'space_utilization': optimal_solution.space_utilization,
        'balance_ratio': optimal_solution.balance_ratio,
        'loaded_ratio': [optimal_solution.loaded_parcels, optimal_solution.total_parcels]
    }
    visualize_loading_solution(solution=optimal_solution, info=sol_info)
