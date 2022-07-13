from itertools import permutations


class Parcel:
	def __init__(self, parcel_type, width, length, height, weight, rotate):
		self.parcel_type = parcel_type
		
		self.width, self.length, self.height = width, length, height
		
		self.weight = weight
		self.rotate = rotate
		
		self.base_area = self.width * self.length
		self.volume = self.get_volume()
		
		self.position = None
		self.state = None
		
		self.loading_sequence = None
		
	def reset_parcels(self):
		self.loading_sequence = None
		self.position = None
		self.state = None
	
	def get_volume(self):
		return self.width * self.height * self.length
	
	def change_layout(self, layout_level):
		"""Randomly generate box orientations (vertical, horizontal,...). Some boxes have oriented constraints."""
		
		if layout_level:
			
			rotate_case = [
				[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 1, 1], [0, 0, 1], [1, 0, 1]
			]
			
			if self.rotate == rotate_case[0]:
				list_layout = list(permutations([self.width, self.length, self.height]))
				level_list = [i / 6 for i in range(6)]
				
				for idx, level in enumerate(level_list):
					self.width, self.length, self.height = \
						list(list_layout[idx]) if layout_level <= level else list(list_layout[-1])
			
			elif self.rotate == rotate_case[1]:
				list_layout = list(permutations([self.width, self.length]))
				level_list = [i / 2 for i in range(2)]
				
				for idx, level in enumerate(level_list):
					self.width, self.length, self.height = \
						list(list_layout[idx]).append(self.height) \
							if layout_level <= level else list(list_layout[-1]).append(self.height)
			
			elif self.rotate == rotate_case[3]:
				list_layout = list(permutations([self.length, self.height]))
				list_layout = [list(i) for i in list_layout]
				
				self.width, self.length, self.height = \
					list_layout[0] + [self.width] if layout_level <= 0.5 else list_layout[1] + [self.width]
			
			elif self.rotate == rotate_case[5]:
				list_layout = list(permutations([self.width, self.height]))
				level_list = [i / 2 for i in range(2)]
				
				for idx, level in enumerate(level_list):
					self.width, self.length, self.height = \
						list(list_layout[idx]).insert(1, self.length) \
							if layout_level <= level else list(list_layout[-1]).insert(1, self.length)