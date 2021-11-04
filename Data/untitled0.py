# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 19:41:03 2021

@author: K
"""

import pandas as pd 
import geopandas as gpd 
import matplotlib.colors
import pycountry
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

background_color = "#fafafa"
#colors
low_c = '#dd4124'
high_c = '#009473'
plt.rcParams["font.family"] = "monospace"
df= pd.read_csv('C:/py/2019.csv')

kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, random_state=4)
kmeans.fit(df[['HS']])
df['kmeans']= kmeans.labels_

geo_temp=df

def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code=pycountry.countries.get(name=country).alpha_3
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE
# create a column for code 
geo_temp['CODE']=alpha3code(geo_temp['country'])


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.columns=['pop_est', 'continent', 'name', 'CODE', 'gdp_md_est', 'geometry']
merge=pd.merge(world,geo_temp,on='CODE')

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['green','blue','red'])
ax = world.plot(figsize=(20,15), linewidth=0.25, edgecolor=background_color, color='lightgray')
ax.axis('off')
ax.set_facecolor(background_color)
merge.plot(column='kmeans',figsize=(20, 15),legend=False,cmap=cmap,ax=ax)


ax.text(-175,112,'Distribution of Happiness Score 2019',fontsize=30,fontweight='bold',color='#323232')
plt.show()
