from modules.space import Space


class Container:
	def __init__(self, width, length, height, max_weight=35000):
		self.container_width = width
		self.container_length = length
		self.container_height = height
		self.container_max_weight = max_weight
		
		self.parcel_inside = []
		self.unfitted_parcel = []
		self.container_space = None
		self.container_volume = self.container_width * self.container_length * self.container_height
	
	def create_container(self):
		self.container_space = \
			[Space(start=[0, 0, 0], end=[self.container_width, self.container_length, self.container_height])]
	
	def reset_container(self):
		self.container_space = [
			Space(start=[0, 0, 0], end=[self.container_width, self.container_length, self.container_height])]
		self.parcel_inside.clear()
		self.unfitted_parcel.clear()
		self.total_weight = 0
	
	def cal_space_ratio(self):
		volume_inside = 0
		for parcel in self.parcel_inside:
			volume_inside += parcel.volume
		
		return volume_inside / self.container_volume
	
	def cal_balance_ratio(self):
		cgx, cgy, cgz, he = 0, 0, 0, 0
		total_volume = 0
		total_weight = 0
		distance = 0
		
		# calculate cgx, cgy, cgz
		for idx, parcel in enumerate(self.parcel_inside):
			cgx += parcel.weight * (parcel.position[0] + parcel.width / 2)
			cgy += parcel.weight * (parcel.position[1] + parcel.length / 2)
			
			total_weight += parcel.weight
			total_volume += parcel.volume
		
		cgx, cgy = cgx / total_weight, cgy / total_weight
		
		# calculate distance
		distance = (1 / 2) * ( \
					abs(cgx - self.container_width / 2) / (self.container_width / 2) + \
					abs(cgy - self.container_length / 2) / (self.container_length / 2))
		
		return (1 - distance) * 100, cgx, cgy
	
	def get_total_parcel_weight(self):
		total_weight = 0
		for parcel in self.parcel_inside:
			total_weight += parcel.weight
		
		return total_weight
	
	def check_duplicate_space(self, ref_space):
		for space in self.container_space:
			if space.start_location == ref_space.start_location \
					and space.end_location == ref_space.end_location:
				return False
		
		return True
	
	def load_parcel(self, space, parcel):
		# update position and state for loaded parcel
		parcel.position, parcel.state = space.start_location, 'loaded'
		
		# update container
		self.parcel_inside.append(parcel)
		
		# update space inside container
		upper_space = \
			Space(start=[space.start_location[0], space.start_location[1], \
			             space.start_location[2] + parcel.height],
			      end=[space.start_location[0] + parcel.width, \
			           space.start_location[1] + parcel.length, space.end_location[2]])
		
		right_space = \
			Space(start=[space.start_location[0] + parcel.width, space.start_location[1], \
			             space.start_location[2]],
			      end=[space.end_location[0], space.start_location[1] + parcel.length, \
			           space.end_location[2]])
		
		front_space = \
			Space(start=[space.start_location[0], space.start_location[1] + parcel.length, \
			             space.start_location[2]],
			      end=space.end_location)
		
		self.container_space.remove(space)
		self.container_space.extend([upper_space, right_space, front_space])
		
		# remove 0 space that generated when parcel fit perfectly to space
		self.container_space = [space for space in self.container_space if space.space_volume != 0]
		
		self.container_space = \
			sorted(self.container_space,
			       key=lambda x: (x.start_location[1], x.start_location[0], x.start_location[2]))
		
		# self.merge_space()
	
	def merge_space(self):
		can_merge = True
		while can_merge:
			new_space = None
			
			for idx, current_space in enumerate(self.container_space):
				
				for idx_, next_space in enumerate(self.container_space):
					if idx == idx_:
						continue
					
					current_space_dim = current_space.get_space_dimension()
					next_space_dim = next_space.get_space_dimension()
					
					# check if 2 spaces have same height and start height
					if current_space.start_location[2] == next_space.start_location[2] \
							and current_space.end_location[2] == next_space.end_location[2]:
						
						# check if it satisfy 2 merging space case
						if current_space.start_location[0] == next_space.start_location[0] \
								and current_space_dim[0] == next_space_dim[0]:
							
							if current_space.end_location[1] == next_space.start_location[1]:
								new_space = Space(start=current_space.start_location,
								                  end=next_space.end_location)
							
							elif current_space.start_location[1] == next_space.end_location[1]:
								new_space = Space(start=next_space.start_location,
								                  end=current_space.end_location)
						
						elif current_space.start_location[1] == next_space.start_location[1] \
								and current_space_dim[1] == next_space_dim[1]:
							
							if current_space.end_location[0] == next_space.start_location[0]:
								new_space = Space(start=current_space.start_location,
								                  end=next_space.end_location)
							
							elif current_space.start_location[0] == next_space.end_location[0]:
								new_space = Space(start=next_space.start_location,
								                  end=current_space.end_location)
					
					if new_space:
						self.container_space.remove(current_space)
						self.container_space.remove(next_space)
						self.container_space.append(new_space)
						
						break
				
				if new_space:
					break
			
			if not new_space:
				can_merge = False