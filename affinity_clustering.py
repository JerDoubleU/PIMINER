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


def score_cluster():
    print()


def getCluster(src, pref, plot, damp, dest):

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

    # fit model
    af = AffinityPropagation(preference=float(pref), damping=float(damp)).fit(X)

    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    n_clusters_ = len(cluster_centers_indices)

    print('Estimated number of clusters: %d' % n_clusters_)

    af_new_rows = []

    for k in range(n_clusters_):
        class_members = labels == k
        cluster_center = X[cluster_centers_indices[k]]

        cluster_score = 0

        for idx, member in enumerate(class_members):
            if member:

                member_text = getRow(raw_df, idx)['text_value'].values.tolist()
                member_sentence_text = str(getRow(raw_df, idx)['raw_sentence'].values)

                if member_sentence_text.__contains__(member_text[0]):
                    cluster_score += 1

                row = {
                    'cluster':k,
                    'cluster_member':idx,
                    'number_of_clusters':n_clusters_,
                    'number_of_members':sum(class_members),
                    'entity_type': getRow(raw_df, idx)['entity_type'],
                    'text_value': getRow(raw_df, idx)['text_value'],
                    'sentence_position': getRow(raw_df, idx)['sentence_position'],
                    'center':cluster_center,
                    'cumulative_cluster_score':cluster_score
                }

                af_new_rows.append(row)

    af_df = pd.DataFrame(af_new_rows)

    print(af_df.head(10))

    try:
        af_df.to_csv(str(dest) + '.csv', index=False)
    except:
        pass

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
    parser.add_argument("--damp", nargs='?', default=.5, help="Damping between 1 and .5")
    parser.add_argument("--dest", nargs='?', help="Filename to save output.")
    parser.set_defaults(plot=False)

    args = parser.parse_args()

    getCluster(args.src, args.pref, args.plot, args.damp, args.dest)
