#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import os
import DimensionalityReduction
from processTXT import getwordcountvector

def amplifydata(arr, amplifyfactor=1):
    result = []
    for item in arr:
        result.append(item*amplifyfactor)
    return result

def getvectordata(datadir, amplifyfactor=1):
    files = os.listdir(datadir)
    vectors = []
    index = 0
    filedict = {}
    for file in files:
        a, b, wordscountratio = getwordcountvector(datadir + file)
        filedict[index] = file
        index += 1
        vectors.append(amplifydata(wordscountratio, amplifyfactor))
    return vectors, filedict

def splitvectors(vectors, filedict, booktitle):
    index = -1
    for k in filedict:
        if filedict[k]==booktitle:
            index = k
            break
    if index == -1:
        print("ERROR! Cannot find book:", booktitle, "in filedict!")
        return None
    i = 0
    newvectors = []
    newfiledict = {}
    for oldindex in range(len(vectors)):
        if oldindex==index:
            shakspeare = vectors[oldindex]
            continue
        newvectors.append(vectors[oldindex])
        newfiledict[i] = filedict[oldindex]
        i += 1
    return shakspeare, newvectors, newfiledict


def computeKNN(k, vectors, point):
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(vectors)
    nearestneighbors = neigh.kneighbors([point], return_distance=False)
    return nearestneighbors

def KNN_main(datadir, pointfilename, k, amplifyfactor):
    originalpoints, originalfiledict = getvectordata(datadir, amplifyfactor)

    # reduce dimensions
    # vectors = dimensionalityreduction.pca_reduction(vectors, 15)
    # vectors = dimensionalityreduction.JL_embedding_reduction(vectors, 100, 50, 0)

    # split test point
    # point, vectors, filedict = splitvectors(vectors, filedict, pointfilename)
    start = time.time()

    correctnnset = set([93, 58, 87, 36, 14, 1])

    count = float(0)
    for i in range(1000):
        vectors = DimensionalityReduction.JL_embedding_reduction(originalpoints, 100, 80, 1, 20)
        # vectors = DimensionalityReduction.pca_reduction(originalpoints, 10)
        point, vectors, filedict = splitvectors(vectors, originalfiledict, pointfilename)
        nn = computeKNN(k, vectors, point)
        for neighbor in nn[0]:
            if neighbor in correctnnset:
                count += 1

    end = time.time()
    print("Correct rate:", count/6000)
    # print("Computing", k, "NN costs", (end-start), "ms!")
    for neighbor in nn[0]:
        print(str(neighbor), filedict[neighbor])

def computeCluster(k, vectors):
    # create kmeans object
    kmeans = KMeans(n_clusters=k)
    # fit kmeans object to data
    kmeans.fit(vectors)
    # print location of clusters learned by kmeans object
    centers = kmeans.cluster_centers_

    # get the label of each point
    # y_km = kmeans.fit_predict(vectors)
    # print(y_km)
    return centers

def cluster_main(datadir, k, amplifyfactor):
    vectors, filedict = getvectordata(datadir, amplifyfactor)

    # reduce dimensions
    vectors = dimensionalityreduction.pca_reduction(vectors, 20)

    start = time.time()
    centers = computeCluster(k, vectors)
    end = time.time()

    print("Computing", k, "clusters costs", (end - start)*1000, "ms!")
    # print(centers)

if __name__=='__main__':
    clusterdatadir = ".\\vectors_cluster\\"
    k = 6
    amplifyfactor = 1e4

    KNN_main(clusterdatadir, "The Complete Works of William Shakespeare.txt", k, amplifyfactor)

    # cluster_main(clusterdatadir, k, amplifyfactor)

    print("Success!")