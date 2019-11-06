#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sklearn.decomposition import PCA
import kNNPCluster
import time
import numpy as np
import math

def pca_reduction(points, k):
    pca = PCA(n_components=k)
    return pca.fit_transform(points)

def test_pca(points, k):
    start = time.time()
    for i in range(100):
        transformedpoints = pca_reduction(points, k)
    end = time.time()

    print("Reducing to", k, "dimensions via PCA costs", (end - start)*10, "ms!")
    # print(transformedpoints)

def compute_k0_JLEmbedding(epsilon, beta, n):
    return (4+2*beta) / (epsilon*epsilon/2 - epsilon*epsilon*epsilon/3) * math.log(n)

# portionnozero表示非0的概率的分母，例如1/3的数不为0，则portionnozero=3
def get_matrix_R(rownum, columnnum, type, portionnozero = 3):
    R = []
    # np.random.seed(1)
    if type==0:  # normal standard distribution
        R = np.random.normal(0, 1, (rownum,columnnum))
    if type==1:
        for i in range(rownum):
            permutation = np.random.permutation(columnnum)
            dtimes = columnnum/portionnozero
            results = []
            for j in range(columnnum):
                 results.append(0)
            j = 0
            while j < dtimes / 2:
                results[permutation[j]] = math.sqrt(portionnozero)
                j += 1
            while j < dtimes:
                results[permutation[j]] = -math.sqrt(portionnozero)
                j += 1
            R.append(results)
    # print(R)
    return R

def JL_embedding_reduction(points, d, k, type, portionnozero=3):
    R = get_matrix_R(d, k, type, portionnozero)
    ApR = np.dot(points, R)
    return np.multiply(ApR, 1/math.sqrt(k))

def test_JL_embedding(points, d, k, type, portionnozero = 3):

    start = time.time()
    for i in range(1000):
        JL_embedding_reduction(points, d, k, type, portionnozero)
    end = time.time()
    if type == 0:
        name = "spherically symmetric case"
    else:
        name = "database friendly"
    print("Reducing to", k, "dimensions via JL-embedding, type:", name, "costs", (end - start), "ms!")
    # print(transformedpoints)

def euclidean_distance(u, v):
    distance = 0
    if len(u) != len(v):
        print("Error,  the length of two vectors is not equal!")
        return None
    for i in range(len(u)):
        distance += math.pow(u[i]-v[i], 2)
    return distance

def JLembedding_success_rate(points, reducedpoints, epsilon):
    totalpair = float(0)
    validpair = float(0)
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            totalpair += 1
            originaldistance = euclidean_distance(points[i], points[j])
            transformeddistance = euclidean_distance(reducedpoints[i], reducedpoints[j])
            if (1 + epsilon)*originaldistance >= transformeddistance >= (1 - epsilon)*originaldistance:
                validpair += 1
    return validpair/totalpair

def test_JLembedding_success_rate(points, k, epsilon):
    # pcapoints = pca_reduction(points, k)
    # print("JL-embedding success rate in PCA, reducing to", k, "dimensions, is:", JLembedding_success_rate(points, pcapoints, epsilon))
    #
    # ssjlpoints = JL_embedding_reduction(points, 100, k, 0)
    # print("JL-embedding success rate in Spherically symmetric case, reducing to", k, "dimensions, is:",
    #       JLembedding_success_rate(points, ssjlpoints, epsilon))
    #
    # type2thirdpoints = JL_embedding_reduction(points, 100, k, 1)
    # print("JL-embedding success rate in database friendly case, distribution 1/3, reducing to", k, "dimensions, is:",
    #       JLembedding_success_rate(points, type2thirdpoints, epsilon))
    ratesum = float(0)
    for i in range(10):
        type1halfpoints = JL_embedding_reduction(points, 100, k, 1, 40)
        ratesum += JLembedding_success_rate(points, type1halfpoints, epsilon)
    print("JL-embedding success rate in database friendly case, distribution 1/x, reducing to", k, "dimensions, is:", ratesum/10)


if __name__=='__main__':
    clusterdatadir = ".\\vectors_cluster\\"
    k = 10
    amplifyfactor = 1e4

    points, filedict = kNNPCluster.getvectordata(clusterdatadir, amplifyfactor)

    test_JLembedding_success_rate(points, 80, 0.4)
    # test_pca(points, 20)
    # test_JL_embedding(points, 100, 20, 1, 1)

    # print(compute_k0_JLEmbedding(0.4, math.log(2.5, 100)-2, 100)) # P[JL-e]>2/3, k0=43


    print("Success!")