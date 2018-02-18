import json

class Cluster():
	def __init__(self, centroid, moves, cluster_size = 10):
		self.centroid = centroid
		self.moves = moves #list of move objects
		self.cluster_size = cluster_size

	"""
	Getters and Setters
	"""
	def append_move(self, move):
		self.moves.append(move)

	def get_centroid(self):
		return self.centroid

	def size(self):
		return self.cluster_size

	def get_moves(self):
		return self.moves

	"""
	Determines the predominant move type of a
	cluster and the percentage that type appears.
	"""
	def get_primary_label(self):
		type_map = self.get_label_percentages()
		max_percentage = 0
		primary_label = ""
		for move_type in type_map:
			if type_map[move_type] > max_percentage:
				max_percentage = type_map[move_type]
				primary_label = move_type
		return primary_label, max_percentage

	"""
	Creates a mapping of percentages for each move type.
	"""
	def get_label_percentages(self):
		type_map = {}
		for move in self.moves:
			if move.get_move_type() in type_map:
				type_map[move.get_move_type()] += 1
			else:
				type_map[move.get_move_type()] = 1.0
		for move_type in type_map:
			type_map[move_type] /= self.size()
		return type_map

	"""
	Print function for information on the cluster. 
	"""
	def get_info(self):
		primary_label, max_percentage = self.get_primary_label()
		print("Cluster Primar2y Type:", primary_label)
		print("\tCluster Size:", self.size())
		print("\t% moves with this type:", max_percentage)
		print("\tCentroid IO:", self.centroid,"\n")
		for move in self.moves:
			print("Move:", move.get_move_name())
			print("Move Type:", move.get_move_type(),"\n")

	"""
	Outputs cluster to json file and cluster's move attributes
	"""
	def to_json(self, filename):
		move_json = {}
		index = 1
		for move in self.moves:
			move_string = "move_" + str(index)
			move_json[move_string] = move.to_dic()
			index += 1
		cluster_json = {"centroid": self.centroid,
						"size": self.size(),
						"moves": move_json}
		print(cluster_json)
		with open(filename, 'w') as outfile: 
			json.dumps(cluster_json, outfile)