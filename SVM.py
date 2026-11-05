import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split,cross_val_score,GridSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,classification_report
from sklearn.ensemble import AdaBoostClassifier,RandomForestClassifier
from sklearn.svm import SVC

df=pd.read_csv("car_evaluation.csv")

df.head()

df["decision"].value_counts()

for column in df.columns:
    print(column,df[column].unique())

df.isnull().sum()

df.duplicated().sum()

df.info()

df.describe()

X=df.drop(["decision"],axis=1)
y=df["decision"]

X=pd.get_dummies(X,dtype=int)
encoder=LabelEncoder()
y=encoder.fit_transform(y)

X.head()

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

models={
    "SVM":SVC(),
    "AdaBoost":AdaBoostClassifier(),
    "Random Forest":RandomForestClassifier()
}
for name,model in models.items():
    model.fit(X_train,y_train) 
    print(name,"training completed")

res={}
for name,model in models.items():
    y_train_pred=model.predict(X_train)
    y_test_pred=model.predict(X_test)

    train_metric={
        "Accuracy":accuracy_score(y_train,y_train_pred),
        "Precision":precision_score(y_train,y_train_pred,average="weighted"),
        "Recall":recall_score(y_train,y_train_pred,average="weighted"),
        "f1":f1_score(y_train,y_train_pred,average="weighted")
    }
    test_metric={
        "Accuracy":accuracy_score(y_test,y_test_pred),
        "Precision":precision_score(y_test,y_test_pred,average="weighted"),
        "Recall":recall_score(y_test,y_test_pred,average="weighted"),
        "f1":f1_score(y_test,y_test_pred,average="weighted")
    }
    acc_test=accuracy_score(y_test,y_test_pred)
    prec_test=precision_score(y_test,y_test_pred,average="weighted")
    rec_test=recall_score(y_test,y_test_pred,average="weighted")
    f1_test=f1_score(y_test,y_test_pred,average="weighted")
    res[name]=[acc_test,prec_test,rec_test,f1_test]
    
    result=pd.DataFrame([train_metric,test_metric],index=["Training","Testing"])
    print(name)
    print(classification_report(y_test,y_test_pred))
    display(result)

for name,model in models.items():
    y_test_pred=model.predict(X_test)
    cm=confusion_matrix(y_test,y_test_pred)
    sns.heatmap(cm,annot=True,fmt="d",cmap="Blues")
    print("confusion matrix of",name)
    plt.show()

cv_result=[]
for name,model in models.items():
    score=cross_val_score(model,X_train,y_train,cv=10,scoring="accuracy")
    cv_result.append({"Model":name,"Average Accuracy":score.mean()})
cv_df=pd.DataFrame(cv_result)
cv_df

param_grid={
    "SVM":{
        "C":[0.1,1,10],
        "kernel":["linear","rbf"],
        "gamma":["auto","scale"]
    },
    "Random Forest":{
        "n_estimators":[50,100,200],
        "max_depth":[None,10,20],
        "min_samples_split":[2,5]
    },
    "AdaBoost":{
        "n_estimators":[50,100,200],
        "learning_rate":[0.01,0.1,1.0]
    }
}

optimized_models={}
for name,model in models.items():
    grid=GridSearchCV(model,param_grid[name],cv=10,scoring="accuracy",n_jobs=-1)  ###model hhi likhna hai yaha bhi
    grid.fit(X_train,y_train)
    optimized_models[name]=grid.best_estimator_
    print(name,grid.best_score_)

results={}          ###sare results nikalke store kerne hai
for name,model in optimized_models.items():
    y_pred=model.predict(X_test)
    acc_test=accuracy_score(y_test,y_pred)
    prec_test=precision_score(y_test,y_pred,average="weighted")
    rec_test=recall_score(y_test,y_pred,average="weighted")
    f1_test=f1_score(y_test,y_pred,average="weighted")
    results[name]=[acc_test,prec_test,rec_test,f1_test]
    print(name)
    print("Accuracy:",acc_test)
    print("Precision:",prec_test)
    print(classification_report(y_test,y_pred))

for name,model in optimized_models.items():
    y_pred=model.predict(X_train)
    cm=confusion_matrix(y_test,y_test_pred)
    sns.heatmap(cm,annot=True,fmt="d",cmap="Blues")
    plt.show()

results_df=pd.DataFrame(results,index=["Acc","Precision","Rec","f1"])
results_df

res_df=pd.DataFrame(res,index=["Acc","Precision","Rec","f1"])
res_df

results_df.plot(kind="bar",figsize=(6,5))
plt.show()
res_df.plot(kind="bar",figsize=(6,5))
plt.show()



