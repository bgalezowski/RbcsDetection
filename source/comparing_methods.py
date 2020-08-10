import numpy as np
from scipy.spatial.distance import euclidean, canberra, mahalanobis

from source.constants import correlation_bound, euclidean_bound, canberra_bound, mahalanobis_bound


def correlation_coefficient(d1, d2):
    d1_average = np.mean(d1)
    d2_average = np.mean(d2)
    nominator = 0
    left_denominator = 0
    right_denominator = 0
    for i in range(0, 126):
        nominator += (d1[i] - d1_average) * (d2[i] - d2_average)
        left_denominator += np.power((d1[i] - d1_average), 2)
        right_denominator += np.power((d2[i] - d2_average), 2)
    result = nominator / np.sqrt(left_denominator * right_denominator)

    if result > correlation_bound:
        return True
    return False


def euclidean_distance(d1, d2):
    result = euclidean(d1, d2)

    if result < euclidean_bound:
        return True
    return False


def canberra_distance(d1, d2):
    result = canberra(d1, d2)

    if result < canberra_bound:
        return True
    return False


def mahalanobis_distance(d1, d2):
    covariance_matrix = np.linalg.pinv(np.cov(np.array([d1, d2]).T))
    result = mahalanobis(d1, d2, covariance_matrix)

    if result < mahalanobis_bound:
        return True
    return False
