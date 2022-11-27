from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import os
from time import time

documents = []


def get_cluster_list(terms_num=None, cluster_num=3):
    for root, dirs, files in os.walk(r"../files"):
        for file in files:
            file_path = os.path.join(root, file)
            f = open(file_path, "r", encoding='utf-8')
            documents.append(BeautifulSoup(f.read(), features="lxml").get_text().replace('\n', '').replace('\r', ''))
            f.close()
    print("%d documents" % len(documents))
    print("%d categories" % cluster_num)

    print("Extracting features from the training dataset using a sparse vectorizer")
    t0 = time()

    vectorizer = TfidfVectorizer(
        max_df=0.5,
        min_df=2,
        stop_words="english",
        use_idf=True,
    )
    X = vectorizer.fit_transform(documents)
    print("done in %fs" % (time() - t0))
    print("n_samples: %d, n_features: %d" % X.shape)
    print()

    km = KMeans(
        n_clusters=cluster_num,
        init="k-means++",
        max_iter=100,
        n_init=1,
        verbose=True,
    )

    print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X)
    print("done in %0.3fs" % (time() - t0))
    print()

    print("Top terms per cluster:")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names_out()
    cluster_list = []
    for i in range(cluster_num):
        print("Cluster %d:" % i, end="")
        tmp = []
        if terms_num is None:
            for ind in order_centroids[i]:
                print(" %s" % terms[ind], end="")
                tmp.append(terms[ind])
        else:
            for ind in order_centroids[i, :int(terms_num)]:
                print(" %s" % terms[ind], end="")
                tmp.append(terms[ind])
        print()
        cluster_list.append(tmp)
    return cluster_list, cluster_num


if __name__ == "__main__":
    clusters, cluster_num = get_cluster_list(50, 3)
    f = open("Kmeans-" + str(cluster_num) + ".txt", "w", encoding='utf-8')
    for i in range(cluster_num):
        f.write(str(clusters[i]) + "\n")
    f.close()
    clusters, cluster_num = get_cluster_list(50, 6)
    f = open("Kmeans-" + str(cluster_num) + ".txt", "w", encoding='utf-8')
    for i in range(cluster_num):
        f.write(str(clusters[i]) + "\n")
    f.close()
    clusters, cluster_num = get_cluster_list(5000, 3)
    f = open("../sentiment/Kmeans-" + str(cluster_num) + ".txt", "w", encoding='utf-8')
    for i in range(cluster_num):
        f.write(str(clusters[i]) + "\n")
    f.close()
    clusters, cluster_num = get_cluster_list(5000, 6)
    f = open("../sentiment/Kmeans-" + str(cluster_num) + ".txt", "w", encoding='utf-8')
    for i in range(cluster_num):
        f.write(str(clusters[i]) + "\n")
    f.close()
