#!/usr/bin/env python -*- coding: utf-8 -*-

from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

import numpy as np
from texeval import TexEval2015

texeval_corpus = TexEval2015()

n=2
sbcs = texeval_corpus.test_subcorpora
sbc = sbcs[n] 
terms = [i[1] for i in texeval_corpus.terms('test', sbc)]

matrix = np.loadtxt(sbc+'.matrix')

n_clusters = int(len(terms)/float(3))
model = AgglomerativeClustering(n_clusters=n_clusters,
                                linkage="average", affinity="cosine")
model.fit(matrix)

print n_clusters

#for i in model.children_:
#    print i

##print n_clusters, len(terms), min(model.labels_), max(model.labels_)

# Get clusters.
for term, clusterid in zip(terms, model.labels_):
    print term, clusterid

print terms


'''
for l in np.arange(model.n_clusters):
    for i in model.labels_ == l:
        print i
    #print matrix[model.labels_ == l].T
    break
''' 

'''
plt.figure()
for l, c in zip(np.arange(model.n_clusters), 'rgbk'):
    plt.plot(matrix[model.labels_ == l].T, c=c, alpha=.5)
plt.show()
'''