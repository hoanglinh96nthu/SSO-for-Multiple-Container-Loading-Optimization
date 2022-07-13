class Space:
	def __init__(self, start: list, end: list):
		self.start_location, self.end_location = start, end
		
		self.space_volume = (self.end_location[0] - self.start_location[0]) * \
		                    (self.end_location[1] - self.start_location[1]) * \
		                    (self.end_location[2] - self.start_location[2])
	
	def get_space_dimension(self):
		return [(self.end_location[0] - self.start_location[0]), \
		        (self.end_location[1] - self.start_location[1]), \
		        (self.end_location[2] - self.start_location[2])]