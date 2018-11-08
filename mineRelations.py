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

    raw_df = pd.read_csv(input_file)

    # name the index
    raw_df.index.names = ['PII_Entity_ID']

    print(raw_df.columns)
    print()

    columns_to_drop = []

    # convert categorical fields to codes
    for field in raw_df.columns:
        if raw_df[field].dtype == 'object':
            columns_to_drop.append(field)
            raw_df['coded_' + str(field)] = raw_df[field].astype('category')
            raw_df['coded_' + str(field)] = raw_df['coded_' + str(field)].cat.codes

    # clean up and preview
    df = raw_df.drop(columns_to_drop, axis=1)
    print(df.head(10))

    # convert to array
    X = np.array(df).astype(np.float)

    af = AffinityPropagation(preference=-100000, verbose=True).fit(X)
    print()
    print(dir(af))

    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    for k in range(n_clusters_):
        class_members = labels == k
        cluster_center = X[cluster_centers_indices[k]]

        for x in X[class_members]:
            for index, row in raw_df.iterrows():
                if x[0] == index:
                    print(row['entity_type'], row['text_value'])
                    print([cluster_center[0], x[0]], [cluster_center[1], x[1]])

    # print()
    # for center in  af.cluster_centers_indices_:
    #     for index, row in raw_df.iterrows():
    #         if center == index:
    #             print(row['entity_type'], row['text_value'])

    # min_pref = -100000
    # max_pref = 0
    #
    # for pref_value in range(min_pref,max_pref):
    #     # fit model
    #     af = AffinityPropagation(preference=pref_value).fit(X)
    #     cluster_centers_indices = af.cluster_centers_indices_
    #     labels = af.labels_
    #     n_clusters_ = len(cluster_centers_indices)

        # print('For Preference: ' + str(pref_value))
        # print('Estimated number of clusters: %d' % n_clusters_)

        # for k in range(n_clusters_):
        #     class_members = labels == k
        #     cluster_center = X[cluster_centers_indices[k]]
        #     print('preference: ' + str(pref_value) + ' clusters: ' + str(n_clusters_) \
        #         + " " + str(X[class_members[k]]))


    # # Plot results
    # plt.close('all')
    # plt.figure(1)
    # plt.clf()
    # # # #
    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # for k, col in zip(range(n_clusters_), colors):
    #     class_members = labels == k
    #     cluster_center = X[cluster_centers_indices[k]]
    #     plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    #     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #              markeredgecolor='k', markersize=14)
    #     for x in X[class_members]:
    #         plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
    #
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()


if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--input_file", help="Choose the csv file to process.")
    args = parser.parse_args()

    getCluster(args.input_file)
