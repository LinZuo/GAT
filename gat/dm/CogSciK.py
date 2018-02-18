import numpy as np


class CogSciK():
    def __init__(self, initial_centroid, cluster_size=10):
        self.centroid = initial_centroid  # np ndarray
        self.cluster_size = cluster_size
        self.cluster = []

    """
    Implementation of clustering algorithm.
    """

    def fit(self, X):
        distance_tuples = []
        for x in X:
            if type(x) is not np.ndarray:
                raise TypeError("Observations must be numpy ndarrays.")
            distance = self.euclidean_distance(self.centroid, x)
            distance_tuples.append((x, distance))
        distance_tuples = self.ordered_sort(distance_tuples)
        closest_points = [x[0] for x in distance_tuples][:self.size()]
        for point in closest_points:
            self.append_to_cluster(point)

    """
    Helper functions for fit().
    """

    def ordered_sort(self, distance_tuples):
        return sorted(distance_tuples, key=lambda x: x[1])

    def euclidean_distance(self, a, b):
        distance = 0.0
        for i in range(0, self.get_num_features()):
            distance += np.linalg.norm(a[i] - b[i])
        return np.sqrt(distance)

    """
    Getters and Setters
    """

    def get_centroid(self):
        return self.centroid

    def size(self):
        return self.cluster_size

    def get_cluster(self):
        return self.cluster

    def get_num_features(self):
        return self.centroid.size

    def append_to_cluster(self, move):
        self.cluster.append(move)
