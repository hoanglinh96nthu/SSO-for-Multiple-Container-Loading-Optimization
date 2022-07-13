import numpy as np


class Input:
	def __init__(self, file_number, problem_number):
		"""Pre-processing and convert .txt data to proper input. """
		# open file and get data from txt file
		iFile = open("dataset/wtpack" + str(file_number) + ".txt", 'r')
		lines = iFile.readlines()  # read each line in txt file
		
		self.ntype = int(lines[1].split()[0])
		self.lines = lines[problem_number * (self.ntype + 2):(problem_number + 1) * (self.ntype + 2)]
		iFile.close()
		
		# convert string to number and list
		self.container_dim = [int(a) for a in lines[0].split()]
		
		# get parcels information
		box = []
		for line in self.lines[2:2 + self.ntype]:
			box.append(line.split())
		
		box = np.array(box, dtype=float)[:, :8]
		self.boxes = box
		
		# generate the constraint (just randomly)
		Top_Bot = np.ones((self.ntype, self.ntype))
		inx1 = np.random.randint(0, self.ntype, self.ntype)
		inx2 = np.random.randint(0, self.ntype, self.ntype)
		Top_Bot[inx1, inx2] = 0


if __name__ == '__main__':
	input_file = Input(file_number=1, problem_number=3)
	boxes = input_file.boxes
	
	for idx, box in enumerate(boxes):
		print(
			f'box {idx} dim: ({box[0]}, {box[2]}, {box[4]}), weight: {box[-1]}, quantities: {box[6]}, rotate: {box[1], box[3], box[5]}')

