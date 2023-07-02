# Import modules and packages
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn')

import os
from scipy.spatial.distance import cdist

# Read data
# cari cara baca data dari uploaded file
# K-MEANS
class KMeans:
    """The k-means algorithm."""

    def __init__(self, n_clusters):
        self.data = pd.DataFrame()
        self.n_clusters = n_clusters
        self.centroids = pd.DataFrame()
        self.clusters = np.zeros(1, dtype=float)
        self.old_centroids = pd.DataFrame()
        self.verbose = False
        self.predictions = []
        self.wcss = pd.Series(dtype=float)

    def train(self, df, verbose):
        self.verbose = verbose
        self.data = df.copy(deep=True)
        self.clusters = np.zeros(len(self.data), dtype=float)  # Perbaikan di sini

        unique_rows = self.data.drop_duplicates()
        unique_rows.reset_index(drop=True, inplace=True)
        np.random.seed(0)  # Mengatur seed generator angka acak
        self.centroids = unique_rows.sample(n=self.n_clusters)
        self.centroids.reset_index(drop=True, inplace=True)

        if self.verbose:
            print("\nRandomly initiated centroids:")
            print(self.centroids)

        # Initialize old centroids as a copy of centroids
        # self.old_centroids = self.centroids.copy(deep=True)

        max_iters = 100
        iter_count = 0
        while iter_count < max_iters:
            self.old_centroids = self.centroids.copy(deep=True)

            for row_i in range(len(self.data)):
                distances = []
                point = self.data.iloc[row_i]

                for row_c in range(len(self.centroids)):
                    centroid = self.centroids.iloc[row_c]
                    distances.append(np.linalg.norm(point - centroid.values))

                self.clusters[row_i] = np.argmin(distances)

            for cls in range(self.n_clusters):
                cls_idx = np.where(self.clusters == cls)[0]

                if len(cls_idx) == 0:
                    self.centroids.loc[cls] = self.old_centroids.loc[cls]
                else:
                    self.centroids.loc[cls] = self.data.iloc[cls_idx].mean()

                if self.verbose:
                    print("\nRow indices belonging to cluster {}: [n={}]".format(cls, len(cls_idx)))
                    print(cls_idx)

            if np.array_equal(self.centroids.values, self.old_centroids.values):
                break

            iter_count += 1

            if self.verbose:
                print("\nOld centroids:")
                print(self.old_centroids)
                print("New centroids:")
                print(self.centroids)
        
        # Compute within-cluster variance (WCSS)
        wcss_value = 0.0
        for cls in range(self.n_clusters):
            cls_idx = np.where(self.clusters == cls)[0]

            if len(cls_idx) > 0:
                cluster_points = self.data.iloc[cls_idx]
                centroid = self.centroids.loc[cls]
                distances = np.linalg.norm(cluster_points - centroid.values, axis=1)
                wcss_value += np.sum(distances ** 2)

            self.wcss[f'Cluster {cls}'] = wcss_value

def perform_clustering(df_scaled, n_clusters, verbose=False):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.train(df_scaled, verbose=verbose)

    clusters = {}
    for cluster in range(n_clusters):
        cluster_data = df_scaled[kmeans.clusters == cluster]
        num_data_points = len(cluster_data)
        clusters[f'Cluster {cluster+1}'] = num_data_points
    
    # Assign cluster labels to the original dataframe
    df_scaled['Cluster'] = kmeans.clusters
    # df_scaled = df_scaled.reset_index()
    
    return clusters, df_scaled


