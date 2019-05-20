import pandas as pd
import re
from sklearn import cluster

path = "C:/Users/Jang/passion_people_jupyter/"
data_top = pd.read_csv(path+"31_df_top.csv",engine="python")
data_bottom = pd.read_csv(path+"32_df_bottom.csv",engine="python")

df_top = data_top[['date','url','label','tags','평균기온..C.']]
df_bottom = data_bottom[['date','url','label','tags','평균기온..C.']]

df_top = df_top.rename(columns = {'평균기온..C.': 'temperature'})
df_bottom = df_bottom.rename(columns = {'평균기온..C.': 'temperature'})

NUM_CLUSTERS=10
kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS).fit(df_top[['temperature']])
labels = kmeans.labels_
df_top['cluster'] = labels

kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS).fit(df_bottom[['temperature']])
labels = kmeans.labels_
df_bottom['cluster'] = labels

# print(df)
df_top.to_csv(path+"41_cluster_df_top.csv",encoding="cp949",index = False)
df_bottom.to_csv(path+"42_cluster_df_bottom.csv",encoding="cp949",index = False)
