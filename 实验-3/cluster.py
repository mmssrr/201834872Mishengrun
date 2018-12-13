from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn import cluster, datasets, mixture, preprocessing
from sklearn.cluster import *
import sklearn
import json

texts = []
labels_true = []
path='data/Tweets.txt'
def readData():

    input = open(path, 'r')

    for line in input.readlines():
        tweets = json.loads(line)

        texts.append(tweets['text'])
        labels_true.append(tweets['cluster'])

readData()

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

vectorizer = CountVectorizer()
X_word2vec = vectorizer.fit_transform(texts)

# KMeans
clf = KMeans(n_clusters=110)
s = clf.fit(X)
labels_predict = clf.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Kmeans NML:', nml)

# Affinity Propagation
af = AffinityPropagation().fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels_predict = af.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Affinity Propagation NML:', nml)

# MeanShift
Xt = preprocessing.scale(X_word2vec.toarray())
clustering = MeanShift(bandwidth=5).fit(Xt)
labels_predict = clustering.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('MeanShift NML:', nml)

# SpectralClustering
sc = SpectralClustering(n_clusters=110)
sc.fit(X)
labels_predict = sc.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Spectral Clustering NML:', nml)

# Ward Hierarchical Clustering
clustering = AgglomerativeClustering(n_clusters=110).fit(X.toarray())
labels_predict = clustering.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Ward Hierarchical Clustering NML:', nml)

# Agglomerative Clustering
clustering = AgglomerativeClustering(linkage='complete', n_clusters=110).fit(X.toarray())
labels_predict = clustering.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Agglomerative Clustering NML:', nml)

# DBSCAN
db = DBSCAN(eps=0.3, min_samples=1).fit(X_word2vec.todense())
labels_predict = db.labels_
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('DBSCAN NML:', nml)

# Gaussian Mixtures
gmm = mixture.GaussianMixture(n_components=110, covariance_type='diag')
gmm.fit(X.toarray())
labels_predict = gmm.predict(X.toarray())
nml = normalized_mutual_info_score(labels_true, labels_predict)
print('Gaussian Mixtures NML:', nml)