import numpy as np


# note this depends on integration with the IO integration
# "moves" refers to the list of the 10 move objects returned by CogSciK
# the Move object has been modified to include a risk and probability

def assign_probabilities(moves):
    for i in range(len(moves)):
        moves[i].probability = np.random.uniform()


def calculate_risks(end_state, moves):
    distances = []
    for move in moves:
        distance = euclidean_distance([end_state["A"], end_state["B"], end_state["C"], end_state["D"], end_state["E"]],
                                      move.IO)
        random_error = np.random.normal(0, 1)
        distance_errored = distance + random_error
        distances.append(distance_errored)
        move.risk = move.probability * distance_errored
    return distances


def resource_encoding(resourcesCategories):
    f = open("resource_vocab.txt", "r")
    resource_vocab = f.readlines()
    f.close()
    vocab_map_indices = {}
    n = len(resource_vocab)

    for i in range(n):
        vocab_map_indices[resource_vocab[i].replace("\n", "")] = i

    one_hot = [0] * n

    for resource in resourcesCategories["low"]:
        one_hot[vocab_map_indices[resource]] = 1
    for resource in resourcesCategories["med"]:
        one_hot[vocab_map_indices[resource]] = 1
    for resource in resourcesCategories["high"]:
        one_hot[vocab_map_indices[resource]] = 1
    return one_hot


# TODO call this right when the simulation is starting
def generate_resource_vocab(moves):
    resource_vocab = set()
    for move in moves:
        for resource in move.resourcesCategories["low"]:
            resource_vocab.add(resource)
        for resource in move.resourcesCategories["med"]:
            resource_vocab.add(resource)
        for resource in move.resourcesCategories["high"]:
            resource_vocab.add(resource)

    f = open("resource_vocab.txt", "w")
    for resource in resource_vocab:
        f.write(resource + "\n")
    f.close()


def euclidean_distance(a, b):
    distance = 0.0
    for i in range(0, len(a)):
        distance += np.linalg.norm(a[i] - b[i])
    return np.sqrt(distance)


if __name__ == "__main__":
    generate_resource_vocab(moves)
