'''
Text analysis on README.md
Clusters 'documents' as denoted by headings:
'## ' and '### '
'''

import os

fullP = '/mnt/h/kbase'
readmeP = os.path.join(fullP, 'README.md')

with open(readmeP) as f:
    lines = f.readlines()

docs = list()
doc = None

for i in lines:
    if i.startswith('# '):
        continue
    elif i.startswith('## '):
        heading = i
    elif i.startswith('### '):
        if not doc is None:
            docs.append(doc)
        doc = ' '.join([heading, i])
    else:
        if not doc is None:
            doc = ' '.join([doc, i])
    if lines.index(i) == len(lines)-1:
        docs.append(doc)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vec = TfidfVectorizer(stop_words='english')
#add stop words like:
# sudo, apt, get, install

V = vec.fit_transform(docs)

k = 7
model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model.fit(V)

import pandas as pd

d = dict()
d['doc'] = docs
d['label'] = model.labels_
df = pd.DataFrame(d)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vec.get_feature_names()

label = [i for i in range(k)]
top_terms = list()

for i in order_centroids:
    top_doc_terms = list()
    for j in i[:5]:
        top_doc_terms.append(terms[j])
    top_doc_terms = ', '.join(top_doc_terms)
    top_terms.append(top_doc_terms)



labels = pd.DataFrame({'label': label, 'top_terms': top_terms})


df = pd.merge(df, labels, left_on='label', right_on='label')
df = df.sort_values(by=['label', 'doc'])

#README_clustered = '\n\n'.join(df.doc.to_list())

README_clustered = list()
label = -1
for index, row in df.iterrows():
    if row['label'] != label:
        README_clustered.append('# {}'.format(row['top_terms']))
        README_clustered.append(row['doc'])
        label += 1
    elif row['label'] == label:
        README_clustered.append(row['doc'])

README_clustP = os.path.join(fullP, 'README_clustered.md')
with open(README_clustP, 'w') as f:
    f.write( '\n\n'.join( README_clustered ) )

print(README_clustP)
