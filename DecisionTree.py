# Python script converted from DecisionTree.ipynb
# Code cell contents and execution order are preserved.

# %%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report
from sklearn.tree import DecisionTreeClassifier,plot_tree   ###DecisionTreeClassifier remember
from sklearn.naive_bayes import GaussianNB

# %%
df=pd.read_csv("Admission_Predict.csv")

# %%
df.head()

# %%
df.isnull().sum()

# %%
df.duplicated().sum()

# %%
df.columns.tolist()

# %%
df=df.drop(["Serial No."],axis=1)

# %%
df.head()

# %%
target_thres=(df["Chance of Admit "].quantile(0.75))
df["Chance of Admit "]=(df["Chance of Admit "]>=target_thres).astype(int)
class_names=["Low","High"]

# %%
df.head()

# %%
X=df.drop("Chance of Admit ",axis=1)
y=df["Chance of Admit "]

# %%
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

# %%
def tree_func(criterion):
    model=DecisionTreeClassifier(criterion=criterion,min_samples_split=10,max_depth=4,min_samples_leaf=5,random_state=42)
    model.fit(X_train,y_train)

    y_train_pred=model.predict(X_train)
    y_test_pred=model.predict(X_test)


    #####remember train and test separetly kerni hai 
    test_metric={
        "Accuracy":accuracy_score(y_test,y_test_pred),
        "Precision":precision_score(y_test,y_test_pred),
        "Recall":recall_score(y_test,y_test_pred),
        "f1":f1_score(y_test,y_test_pred)
    }
    train_metric={
        "Accuracy":accuracy_score(y_train,y_train_pred),
        "Precision":precision_score(y_train,y_train_pred),
        "Recall":recall_score(y_train,y_train_pred),
        "f1":f1_score(y_train,y_train_pred)
    }
    result=pd.DataFrame([train_metric,test_metric],index=["Train metrcis","Test Metrics"])
    display(result)
    return model,y_train,y_test,y_train_pred,y_test_pred,result

# %%
###entropy

# %%
dt_entropy,entropy_train,entropy_test,entropy_train_pred,entropy_test_pred,result=tree_func("entropy")

# %%
cm=confusion_matrix(y_test,entropy_test_pred)
sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)

# %%
plt.figure(figsize=(15,10))
plot_tree(dt_entropy,feature_names=X_train.columns,class_names=class_names,filled=True)
plt.show()

# %%
##gini

# %%
dt_gini,gini_train,gini_test,gini_train_pred,gini_test_pred,results=tree_func("gini")

# %%
cm=confusion_matrix(y_test,gini_test_pred)
sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)
plt.xlabel("predicted")
plt.ylabel("actual")
plt.show()

# %%
plt.figure(figsize=(15,10))
plot_tree(dt_gini,feature_names=X_train.columns,filled=True,class_names=class_names)
plt.show()

# %%
##Naive bayes

# %%
nb=GaussianNB()

# %%
x_high_low=X.copy()
for feature in X.columns:
    x_high_low[feature]=np.where(x_high_low[feature]>=x_high_low[feature].median(),"high","low")
x_high_low["Chance of Admit "]=y.values

likelihood_tab={}
for col in X.columns:
    likelihood_tab[col]=pd.crosstab(x_high_low[col],x_high_low["Chance of Admit "],normalize=True)
    print(col)
    print(likelihood_tab[col])
output_df=y.value_counts(normalize=True)
print(output_df)

# %%
nb.fit(X_train,y_train) 
y_train_pred=nb.predict(X_train)
y_test_pred=nb.predict(X_test)

# %%
test_metric={
    "Accuracy":accuracy_score(y_test,y_test_pred),
    "Precision":precision_score(y_test,y_test_pred),
    "Recall":recall_score(y_test,y_test_pred),
    "f1":f1_score(y_test,y_test_pred)
}
train_metric={
    "Accuracy":accuracy_score(y_train,y_train_pred),
    "Precision":precision_score(y_train,y_train_pred),
    "Recall":recall_score(y_train,y_train_pred),
    "f1":f1_score(y_train,y_train_pred)
}

# %%
result_nb=pd.DataFrame([train_metric,test_metric],index=["Train metrcis","Test Metrics"])
display(result_nb)

# %%
cm=confusion_matrix(y_test,gini_test_pred)
sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)
plt.xlabel("predicted")
plt.ylabel("actual")
plt.show()

# %%
result.plot(kind="bar",figsize=(6,4))
plt.show()
results.plot(kind="bar",figsize=(6,4))
result_nb.plot(kind="bar",figsize=(6,4))

# %%

