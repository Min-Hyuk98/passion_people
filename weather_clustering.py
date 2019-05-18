import pandas as pd
import re
from sklearn import cluster

path = "C:/Users/Jang/passion_people_jupyter/"
data_f = pd.read_csv(path+"df_up2.csv",engine="python")

df = data_f[['date','url','label','tags','평균기온..C.']]
df = df.rename(columns = {'평균기온..C.': 'temperature'})

NUM_CLUSTERS=10
kmeans = cluster.KMeans(n_clusters=NUM_CLUSTERS).fit(df[['temperature']])
labels = kmeans.labels_
df['cluster'] = labels
# print(df)
df.to_csv(path+"cluster_df_up2.csv",encoding="cp949",index = False)
