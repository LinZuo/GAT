"""
This example solves the clustering problem that inspired CogSciK: 
clustering an actor's possible moves and their respective attributes 
based on the moves' IO values and the initial centroid, which is the 
actor's current IO vector. To perform the clustering, we create
a custom Move Object that we parse each move's attributes into, 
and then we perform the CogSciK clustering based on the IO attribute.
"""
import utils as u
import numpy as np
from gat.dm.CogSciK import CogSciK
from gat.dm.Cluster import Cluster

"""
We will first read in the moves from a csv and prepare it for training 
the CogSciK clustering algorithm. Below X is the training set and move_map
is a map of move's IO to its respective object. Note the IO vectors in 
the moves csv are chars between "A"-"E", so I convert them to numbers with
the IO_random_sampler function. CogSciK is built to take in numpy ndarrays.
For more information read the comments on the functions in utils.py.
"""

data = u.read_moves("moves.csv")
move_map = u.map_moves(data)
X = u.build_training_set(move_map)

"""
Now we initialize the CogSciK object with an initial centroid value and 
fit the object to the training set, X. We save the cluster of moves for 
further analysis.
"""
actors_IO = ['A', 'B', 'C', 'D', 'E']
actors_IO = np.array([u.IO_random_sampler(x) for x in actors_IO])
cluster_size = 10
csk = CogSciK(actors_IO, cluster_size)
csk.fit(X)
moves = csk.get_cluster()

"""
After saving the closest moves as a list of numpy arrays, each array
corresponding to a move object, we will reconvert these arrays to their
respective move objects and then conduct analysis on the cluster of move
objects. We do this with a custom cluster object (in Cluster.py).
"""
moves = u.remap_moves(moves, move_map)
cluster = Cluster(actors_IO, moves, cluster_size)
cluster.get_info()

