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

def getRow(df, index):
    try:
        return df.iloc[[index]]
    except:
        return [['NONE']]


def getCluster(src, pref, plot):

    raw_df = pd.read_csv(src)

    # print(len(raw_df))
    # print(raw_df.columns)
    # print(raw_df.head(10))
    # print()

    columns_to_drop = []

    # convert categorical fields to codes
    for field in raw_df.columns:
        if raw_df[field].dtype == 'object':
            columns_to_drop.append(field)
            raw_df['coded_' + str(field)] = raw_df[field].astype('category')
            raw_df['coded_' + str(field)] = raw_df['coded_' + str(field)].cat.codes

    df = raw_df.drop(columns_to_drop, axis=1)
    # print(df.head(10))

    # convert to array
    X = np.array(df).astype(np.float)

    af_new_rows = []

    # fit model
    af = AffinityPropagation(preference=float(pref)).fit(X)

    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    print('Estimated number of clusters: %d' % n_clusters_)

    for k in range(n_clusters_):
        class_members = labels == k
        cluster_center = X[cluster_centers_indices[k]]

        for x in X[class_members]:

            print(k, labels, x)

            # columns = ['entity_type', 'text_value']
            #
            # print('Center: ', x)
            # print('Types:')
            # try:
            #     [print(getRow(raw_df, a)[columns].values[0][0], \
            #         getRow(raw_df, a)[columns].values[0][1]) for a in x]
            # except:
            #     continue
            # print()

    if plot:
        # Plot results
        plt.close('all')
        plt.figure(1)
        plt.clf()
        # # #
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


if __name__ == "__main__":

    # # parse command-line args
    parser = argparse.ArgumentParser(description='file')
    parser.add_argument("--src", help="Choose the csv file to process.")
    parser.add_argument("--pref", help="Preference value")
    parser.add_argument('--plot', dest='plot', action='store_true')
    parser.set_defaults(plot=False)

    args = parser.parse_args()

    getCluster(args.src, args.pref, args.plot)
