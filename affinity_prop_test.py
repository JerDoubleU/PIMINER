


# get clusters
def getCluster(dataframe):
    X = np.array(dataframe)

    # Create a graph model
    edge_model = covariance.GraphLassoCV()
    # # #
    # # # Train the model
    with np.errstate(invalid='ignore'):
        edge_model.fit(X)

    print(dir(edge_model))
    # #
    # Build clustering model using Affinity Propagation model
    _, labels = cluster.affinity_propagation(edge_model.covariance_)
    num_labels = labels.max()
