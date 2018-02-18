import gat.dm.utils as u
import numpy as np
from gat.dm.CogSciK import CogSciK

def io(initial_io):
    data = u.read_moves("./static/resources/dm_data/moves.csv")
    move_map = u.map_moves(data)
    X = u.build_training_set(move_map)

    actors_IO = np.array([u.IO_random_sampler(x) for x in initial_io])
    cluster_size = 10
    csk = CogSciK(actors_IO, cluster_size)
    csk.fit(X)
    moves = csk.get_cluster()

    return u.remap_moves(moves, move_map)