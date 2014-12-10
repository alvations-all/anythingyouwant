#!/usr/bin/env python -*- coding: utf-8 -*-

from sklearn.feature_extraction.image import grid_to_graph
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

import numpy as np
from texeval import TexEval2015

import random

random.seed(3)

texeval_corpus = TexEval2015()

n=2
sbcs = texeval_corpus.test_subcorpora
sbc = sbcs[n] 
terms = [row[1] for row in texeval_corpus.terms('test', sbc)]

matrix = np.loadtxt(sbc+'.matrix')

n_clusters = int(len(terms)/float(3))
model = AgglomerativeClustering(n_clusters=n_clusters,
                                linkage="ward", affinity="euclidean")
model.fit(matrix)

print n_clusters, len(terms)
'''
print model.children_[500]
print model.children_[520]
print model.children_[1520]
'''
l = len(terms)

#print model.n_components_

#print model.n_leaves_

#print len(model.children_)
#print model.children_

#for row in model.children_:
#print row


for row in model.children_:
    if int(row[0]) > l or int(row[1]) > l:
        print row
    else:
            
        try:
            t1 = terms[row[0]]
            t2 = terms[row[1]]
            print row, t1, " ||| ", t2
        except:
            continue

'''
print n_clusters, len(terms), min(model.labels_), max(model.labels_)


# Get clusters.
for term, clusterid in zip(terms, model.labels_):
    print clusterid, term
'''









'''
for l in np.arange(model.n_clusters):
    for row in model.labels_ == l:
        print row
    #print matrix[model.labels_ == l].T
    break
''' 

'''
plt.figure()
for l, c in zip(np.arange(model.n_clusters), 'rgbk'):
    plt.plot(matrix[model.labels_ == l].T, c=c, alpha=.5)
plt.show()
'''