# Python script converted from Clustering.ipynb
# Code cell contents and execution order are preserved.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.cluster import KMeans,AgglomerativeClustering,BisectingKMeans
from scipy.cluster.hierarchy import dendrogram,linkage
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,classification_report,silhouette_score
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# %%
df=pd.read_csv("iris.csv")

# %%
df.head()

# %%
y=df["Species"]

# %%
df=df.drop(["Id","Species"],axis=1)

# %%
df.head()

# %%
X=df.copy()

# %%
scaler=StandardScaler()
X=scaler.fit_transform(df)      ###don't forget standardscaler

# %%
inertia=[]
for k in range(1,11):
    model=KMeans(n_clusters=k,random_state=42,n_init=10)
    model.fit(X)             ####### sirf X hi pass hota hai 
    inertia.append(model.inertia_)
plt.figure(figsize=(6,5))
plt.plot(range(1,11),inertia,marker="o")
plt.show()

# %%
model=KMeans(n_clusters=3,random_state=42,n_init=10)
y_pred=model.fit_predict(X)    #####X pass kerna hai /same variable ka use karo, model likha hai pehle to model hi likho don't make such mistake
result_df=df.copy() 
result_df["Kmean"]=y_pred
result_df.head()

# %%
plt.figure(figsize=(6,5))
plt.scatter(X[:,2],X[:,3],c=y_pred)       ####X use kerna hai 
plt.scatter(model.cluster_centers_[:,2],model.cluster_centers_[:,3],color="red",marker="X",s=200) ##cluster_centers_,    
#X nhi likhte hai isme or color hota hai direct not use y_pred

# %%
Z=linkage(X,method="ward")
plt.figure(figsize=(6,5))
dendrogram(Z,truncate_mode="lastp",p=20)
plt.show()

# %%
model=AgglomerativeClustering(n_clusters=3,linkage="ward")    ###linkage likhte hai naki random state wagera
y_Apred=model.fit_predict(X)
result_df["Agglomarative"]=y_Apred
result_df.head()

# %%
plt.figure(figsize=(6,5))
plt.scatter(X[:,2],X[:,3],c=y_Apred)
plt.show()

# %%
display(result_df["Kmean"].value_counts())                                ####ye print kerna nhi bhulna hai 
print(result_df["Agglomarative"].value_counts())

# %%
y=y.loc[df.index]   ###don't forget this

# %%
ct_k=pd.crosstab(y,y_pred,rownames=["Species"],colnames=["KMean"])         ###y,y_pred use hota hai
display(ct_k)

# %%
ct_k.plot(kind="bar",figsize=(6,5),color=["green","yellow","blue"])      ##color bhi hum humare hisab se de sakte hai
plt.show()

# %%
# ct_k=pd.crosstab(X,y_pred)
# ct_k.plot(kind="bar",figsize=(6,5))

# %%
print("silhoute score of kmean clusters",round(silhouette_score(X,y_pred),2))     ### yaha X,y_pred use hota hai 
print("silhouette score of Agglomarative",round(silhouette_score(X,y_Apred),2))

# %%
Bmodel = BisectingKMeans(n_clusters=3,random_state=42)            ####remember this method
y_Bpred = model.fit_predict(X)
result_df["Bmodel"]=y_Bpred
result_df.head()

# %%

