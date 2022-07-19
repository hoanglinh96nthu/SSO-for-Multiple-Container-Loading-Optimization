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
	sorted_parcels = sorted(list_parcels, key=lambda x: x.loading_sequence)
	
	# looping for space in container to load parcels
	for idx, parcel in enumerate(sorted_parcels):
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
	
	return container
