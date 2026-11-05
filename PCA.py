# Python script converted from PCA.ipynb
# Code cell contents and execution order are preserved.

# %%
import pandas as pd 
import numpy as  np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report
from sklearn.neighbors import KNeighborsClassifier

# %%
df=pd.read_csv("Wine.csv")

# %%
df.head()

# %%
print(df.shape[0])
print(df.shape[1])

# %%
df["Customer_Segment"].value_counts()

# %%
df["Customer_Segment"].unique()

# %%
for column in df.columns:
    print(column,df[column].count())

# %%
X=df.drop(["Customer_Segment"],axis=1)
y=df["Customer_Segment"]

# %%
scaler=StandardScaler()       ###pca ke liye scaling kerni padti hai
X_scal=scaler.fit_transform(X)

# %%
X_train,X_test,y_train,y_test=train_test_split(X_scal,y,test_size=0.2,random_state=42)

# %%
model=KNeighborsClassifier()
model.fit(X_train,y_train)
y_train_pred=model.predict(X_train)
y_test_pred=model.predict(X_test)

# %%
ktrain_acc=accuracy_score(y_train,y_train_pred)
ktrain_pre=precision_score(y_train,y_train_pred,average="weighted")
ktrain_rec=recall_score(y_train,y_train_pred,average="weighted")
ktrain_f1=f1_score(y_train,y_train_pred,average="weighted")

ktest_acc=accuracy_score(y_test,y_test_pred)
ktest_pre=precision_score(y_test,y_test_pred,average="weighted")
ktest_rec=recall_score(y_test,y_test_pred,average="weighted")
ktest_f1=f1_score(y_test,y_test_pred,average="weighted")

# %%
result=pd.DataFrame([ktrain_acc,ktrain_pre,ktrain_rec,ktrain_f1,ktest_acc,ktest_pre,ktest_rec,ktest_f1],
                   index=["Train accuracy","Train precision","Train recall","Train f1","Test acc","Test precision","Test rec","Test f1"],
                   columns=["Result"])
result.T

# %%
cm=confusion_matrix(y_test,y_test_pred)
sns.heatmap(cm,annot=True,cmap="Blues",fmt="d")

# %%
##########remember

pca_full=PCA()
pca_full.fit(X_scal)
plt.figure(figsize=(6,5))
plt.plot(range(1,14),pca_full.explained_variance_ratio_,marker="o")

# %%
pca=PCA(n_components=2)  ###don't forget n_components
X_pca=pca.fit_transform(X_scal)
pca_df=pd.DataFrame(X_pca,columns=["PC1","PC2"])
pca_df["Quality"]=y.values

# %%
pca_df.head()

# %%
X_train,X_test,y_train,y_test=train_test_split(X_pca,y,test_size=0.2,random_state=42)
model.fit(X_train,y_train)
y_train_pred=model.predict(X_train)
y_test_pred=model.predict(X_test)

# %%
ptrain_acc=accuracy_score(y_train,y_train_pred)
ptrain_pre=precision_score(y_train,y_train_pred,average="weighted") ###average="weighted" ata hai yaad rakho 
ptrain_rec=recall_score(y_train,y_train_pred,average="weighted")
ptrain_f1=f1_score(y_train,y_train_pred,average="weighted")

ptest_acc=accuracy_score(y_test,y_test_pred)
ptest_pre=precision_score(y_test,y_test_pred,average="weighted")
ptest_rec=recall_score(y_test,y_test_pred,average="weighted")
ptest_f1=f1_score(y_test,y_test_pred,average="weighted")

# %%
results=pd.DataFrame([ptrain_acc,ptrain_pre,ptrain_rec,ptrain_f1,ptest_acc,ptest_pre,ptest_rec,ptest_f1],
                   index=["Train accuracy","Train precision","Train recall","Train f1","Test acc","Test precision","Test rec","Test f1"],
                   columns=["Result"])
results.T

# %%
cm=confusion_matrix(y_test,y_test_pred)
sns.heatmap(cm,annot=True,cmap="Blues",fmt="d")

# %%
plt.figure(figsize=(6,5))
plt.scatter(X_scal[:,0],X_scal[:,1],color="orange",alpha=0.6)        ##yaha wale me color me color hi pass kerna hota hai
plt.show()
plt.scatter(X_pca[:,0],X_pca[:,1],color="green",alpha=0.6)
plt.show()

# %%
plt.figure(figsize=(6,4))
plt.bar(["Before PCA","After"],[ktest_acc,ptest_acc],color=["blue","green"])
plt.title("Accuracy compare")
plt.show()
plt.figure(figsize=(6,4))
plt.bar(["Before","After"],[ktest_pre,ptest_pre],color=["blue","green"])
plt.title("Precision compare")
plt.show()
plt.figure(figsize=(6,4))
plt.bar(["Before","After"],[ktest_rec,ptest_rec],color=["blue","green"])

# %%
result_df=pd.DataFrame(result)

# %%
result_df.plot(kind="bar",figsize=(6,5))     ##direct result se graph nhi ban raha tha to ek or df banaya or uski help se plot kiye 

# %%

