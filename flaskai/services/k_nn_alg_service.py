from flaskai.algorithms.k_nn_alg import KNearestNeighbors


class KnnService:

    k_nearest_neighbour = KNearestNeighbors()

    '''
        returns the place and the accuarcy of the result
    '''
    def knn(self, investments, medium_age, wins, equals, defeats, goals):
        return self.k_nearest_neighbour.knn(investments, medium_age, wins, equals, defeats, goals)
