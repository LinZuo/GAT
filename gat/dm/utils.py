import csv

import numpy as np

from gat.dm.Move import Move

"""
General Function for reading in the moves.csv (converted from XLSX).
Each move is read in as a dictionary with keys corresponding to the csv
header columns, and all moves are returned together in an ordered list.
"""


def read_moves(filename):
    n_col = 13
    move_parts = ["code", "move_name", "move_type", "warmth", "affinity",
                  "legitimacy", "dominance", "competence",
                  "ph", "low_resources", "med_resources",
                  "high_resources", "infrastructure"]
    moves = []
    with open(filename, "rU") as csvfile:
        move_rows = csv.reader(csvfile, dialect="excel")
        next(move_rows)
        next(move_rows)
        for move_row in move_rows:
            move = {}
            if move_row[0] != "":
                for i in range(0, n_col):
                    move[move_parts[i]] = move_row[i]
                moves.append(move)
    return moves


"""
Creates a map of unique IO keys mapped to their respective move objects.
Move objects are initialized with all of their attributes from moves.csv.
"""


def map_moves(moves):
    move_map = {}
    IO_string_set = set()
    for move in moves:
        IO_list = [IO_random_sampler(x) for x in
                   [move["warmth"],
                    move["affinity"], move["legitimacy"],
                    move["dominance"], move["competence"]]]
        IO_string = list_to_string(IO_list)
        while IO_string in IO_string_set:
            IO_list = [IO_random_sampler(x) for x in
                       [move["warmth"],
                        move["affinity"], move["legitimacy"],
                        move["dominance"], move["competence"]]]
            IO_string = list_to_string(IO_list)
        IO_string_set.add(IO_string)
        IO_string = list_to_string(IO_list)
        # TODO fill category in csv file. Random category for now. Blocks Emotional pole from working correctly.
        move_map[IO_string] = Move(move["code"],
                                   move["move_name"],
                                   move["move_type"],
                                   IO_list,
                                   move["ph"],
                                   [resource.strip() for resource in move["low_resources"].replace(",", " ").split()],
                                   [resource.strip() for resource in move["med_resources"].replace(",", " ").split()],
                                   [resource.strip() for resource in move["high_resources"].replace(",", " ").split()],
                                   move["infrastructure"],
                                   category='Build political infrastructure')
    return move_map


"""
Builds a training set (numpy matrix) of the IO values
of all the moves, represented as numpy arrays.
"""


def build_training_set(move_map):
    X = np.zeros(shape=(len(move_map), 5))
    index = 0
    for move in move_map:
        X[index] = np.array(string_to_list(move))
        index += 1
    return X


"""
Helper function for converting the labels A-E for each Pole value
to a random float within the range specified by the labels.
"""


def IO_random_sampler(label):
    return {
        "A": random_float(-0.8, -0.6),
        "B": random_float(-0.5, -0.3),
        "C": random_float(-0.2, 0.2),
        "D": random_float(0.3, 0.5),
        "E": random_float(0.6, 0.8)
    }.get(label, 0.00)


def random_float(a, b):
    return round(np.random.uniform(a, b), 8)


"""
Helper functions for converting between different 
representations of the IO values.
"""


def list_to_string(IO_list):
    return ",".join([str(x) for x in IO_list])


def string_to_list(IO_string):
    return [float(x) for x in IO_string.split(",")]


def nparray_to_string(IO_nparray):
    return list_to_string(IO_nparray.tolist())


"""
Maps the list of np arrays representing each move in the 
centroid's cluster to their respective move objects.
"""


def remap_moves(moves, move_map):
    move_strings = [nparray_to_string(move) for move in moves]
    move_objects = [move_map[move_string] for move_string in move_strings]
    return move_objects


def formatMeasure(measure):
    newMeasure = ""
    for ch in measure:
        if ch == " ":
            newMeasure += "_"
        else:
            newMeasure += ch
    return newMeasure.strip().lower()
