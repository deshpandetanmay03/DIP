from modules import pygame, KMeans, np, pd, plt, silhouette_score

def add_point(points, events):
    # Handle the events
        for event in events:
            # If the user clicks the close button, exit the loop
            if event.type == pygame.QUIT:
                return 0
            # If the user clicks the mouse button, get the position and append it to the points list
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                points.append(pos)

def optimal_clusters(points, limit):
    data = pd.DataFrame({"x": [p[0] for p in points], "y": [p[1] for p in points]})
    # Define range of values for k
    k_range = range(2, min(limit, len(points)))

    # Apply k-means clustering for each value of k and calculate average silhouette score
    sil_scores = []
    for k in k_range:
        km = KMeans(n_clusters=k, n_init='auto')
        km.fit(data)
        labels = km.labels_
        sil_score = silhouette_score(data, labels)
        sil_scores.append(sil_score)

    # Assuming that `sil_scores` and `k_range` are defined as in your code snippet
    plt.plot(k_range, sil_scores)
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette score')
    plt.title('Silhouette scores for different values of k')
    plt.show()

    return k_range[np.argmax(sil_scores)]


def clustered(points, limit=15):
    if len(points) == 1:
        return (0,), 1
    if len(points) == 2:
        return (0, 1), 2
    clusters = optimal_clusters(points, limit=limit)

    # Create some sample data
    points = np.array(points)

    # Create a KMeans instance with the desired number of clusters
    kmeans = KMeans(n_clusters=clusters, n_init='auto')

    # Fit the model to the data
    kmeans.fit(points)

    # Get the cluster assignments for each point
    labels = kmeans.labels_

    # Print the results
    return labels, clusters
