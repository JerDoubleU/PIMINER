#!/usr/bin/env python3

import argparse # # inorder to port to command line
import os # # system controls
from sklearn import covariance, cluster # attempt at clustering
from sklearn.cluster import AffinityPropagation
import pandas as pd
import numpy as np
import sklearn.metrics as met
import matplotlib.pyplot as plt
from itertools import cycle


def getCluster(input_file):

    readFrame = pd.read_csv(input_file)

    readFrame["text_value"] = readFrame["text_value"].astype('category')
    readFrame["entity_type"] = readFrame["entity_type"].astype('category')

    readFrame["text_value_category"] = readFrame["text_value"].cat.codes
    readFrame["entity_type_category"] = readFrame["entity_type"].cat.codes
    readFrame["subtee_len"] = len(readFrame['subtree'])
    readFrame["num_lefts"] = len(readFrame['lefts'])
    readFrame["num_rights"] = len(readFrame['rights'])

    # print(readFrame.dtypes)

    # # likely need to save entity values and category codes in list

    readFrame = readFrame.drop(['end_position',
        'entity_type',
        'lefts',
        'rights',
        'subtree',
        'text_value'], axis=1)

    # print(readFrame.dtypes)

    X = np.array(readFrame).astype(np.float)
    #
    af = AffinityPropagation(preference=-50).fit(X)

    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_

    n_clusters_ = len(cluster_centers_indices)

    # print('Estimated number of clusters: %d' % n_clusters_)
    # print("Homogeneity: %0.3f" % met.homogeneity_score(labels_true, labels))
    # print("Completeness: %0.3f" % met.completeness_score(labels_true, labels))
    # print("V-measure: %0.3f" % met.v_measure_score(labels_true, labels))
    # print("Adjusted Rand Index: %0.3f"
    #       % met.adjusted_rand_score(labels_true, labels))
    # print("Adjusted Mutual Information: %0.3f"
    #       % met.adjusted_mutual_info_score(labels_true, labels))
    # print("Silhouette Coefficient: %0.3f"
    #       % met.silhouette_score(X, labels, metric='sqeuclidean'))

    # Plot results
    plt.close('all')
    plt.figure(1)
    plt.clf()
    #
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        class_members = labels == k
        cluster_center = X[cluster_centers_indices[k]]
        plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
        for x in X[class_members]:
            plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

    # # Create a graph model
    # edge_model = covariance.GraphLassoCV()
    #
    # # # # Train the model
    # with np.errstate(invalid='ignore'):
    #     edge_model.fit(X)

    # # Build clustering model using Affinity Propagation model
    # _, labels = cluster.affinity_propagation(edge_model.covariance_)
    # num_labels = labels.max()


if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--input_file", help="Choose the csv file to process.")
    args = parser.parse_args()

    getCluster(args.input_file)
