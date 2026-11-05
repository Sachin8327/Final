import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler,LabelEncoder,PolynomialFeatures
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore",category=UserWarning)

df=pd.read_csv("housing.csv")

df.head()

df.info()

df.describe()

df.duplicated().sum()

df.isnull().sum()

df["total_bedrooms"]=df["total_bedrooms"].fillna(df["total_bedrooms"].mean())      ### isko dekho

df.isnull().sum()

df=df.drop(["latitude","longitude","ocean_proximity"],axis=1)

cm=df.corr(numeric_only=True)
sns.heatmap(cm,annot=True,fmt=".2f",cmap="coolwarm")

X=df[["median_income"]]                ###df likhna bbhule to chhud jaoge
y=df["median_house_value"]

model=LinearRegression()

split=[]
for percen in np.arange(0.1,1.0,0.1):
    X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=percen,random_state=91)
    model.fit(X_train,y_train)
    y_train_pred=model.predict(X_train)
    y_test_pred=model.predict(X_test)
    train_error=mean_squared_error(y_train,y_train_pred)
    test_error=mean_squared_error(y_test,y_test_pred)
    split.append([percen,train_error,test_error])      ##tino ko append kerna hai , ([]) me pass kerna hota hai 
split_df=pd.DataFrame(split,columns=["Training%","Train error","Test error"])      ####sirf split likhna hai 

split_df["Difference"]=abs(split_df["Train error"]-split_df["Test error"])
split_df["Difference"]=round(split_df["Difference"],2)
best_split=split_df.sort_values("Difference").iloc[0]["Training%"]    ###difference sort me pass hoga
best_split

plt.figure(figsize=(6,5))
plt.plot(split_df["Training%"],split_df["Train error"],marker="o")
plt.plot(split_df["Training%"],split_df["Test error"],marker="o")
plt.show()

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=best_split,random_state=91)

model.fit(X_train,y_train)
y_train_pred=model.predict(X_train)
y_test_pred=model.predict(X_test)

ltrain_mse=mean_squared_error(y_train,y_train_pred)
ltrain_mae=mean_absolute_error(y_train,y_train_pred)
ltrain_r2=r2_score(y_train,y_train_pred)
ltest_mse=mean_squared_error(y_test,y_test_pred)
ltest_mae=mean_absolute_error(y_test,y_test_pred)
ltest_r2=r2_score(y_test,y_test_pred)

result=pd.DataFrame([ltrain_mse,ltrain_mae,ltrain_r2,ltest_mse,ltest_mae,ltest_r2],
                    index=["Train mse","Train mae","Train r2","Test mse","Test mae","Test r2"],
                    columns=["Result"])
result

plt.figure(figsize=(10,6))
plt.scatter(X_train,y_train,color="green",alpha=0.6)
plt.scatter(X_test,y_test,color="orange",alpha=0.2)
plt.scatter(X_train,y_train_pred,color="blue",alpha=0.2)
plt.scatter(X_test,y_test_pred,color="red",alpha=0.2)

print(model.coef_)
print(model.intercept_)

# f1=int(input("enter median income"))
# user_input=np.array([[f1]])
# prediction=model.predict(user_input)
# print(prediction)

X=df[["median_income","total_rooms"]]
y=df["median_house_value"]

poly=PolynomialFeatures(degree=2)
X_poly=poly.fit_transform(X)

X_train,X_test,y_train,y_test=train_test_split(X_poly,y,test_size=best_split,random_state=91)
model.fit(X_train,y_train)
y_train_pred=model.predict(X_train)
y_test_pred=model.predict(X_test)

ptrain_mse=mean_squared_error(y_train,y_train_pred)
ptrain_mae=mean_absolute_error(y_train,y_train_pred)
ptrain_r2=r2_score(y_train,y_train_pred)
ptest_mse=mean_squared_error(y_test,y_test_pred)
ptest_mae=mean_absolute_error(y_test,y_test_pred)
ptest_r2=r2_score(y_test,y_test_pred)

results=pd.DataFrame([ptrain_mse,ptrain_mae,ptrain_r2,ptest_mse,ptest_mae,ptest_r2],
                     index=["Train mse","Train mae","Train r2","Test mse","Test mae","Test r2"],
                     columns=["Result"])  ###remember columns
results.T

# plt.bar(["ltest_mse","ptest_mse"],[ltest_mse,ptest_mse],color=["blue","green"])            yaad rakho kya likha kese likha hai 
plt.bar(["ltest_mse","ptest_mse"],[ltest_mse,ptest_mse],color=["blue","green"])       ####plt.bar ayega  
plt.ylabel("MSE"),  
plt.show()
plt.bar(["ltest_mae","ptest_mae"],[ltest_mae,ptest_mae],color=["blue","green"])
plt.ylabel("MAE")
plt.show()
plt.bar(["ltest_r2","ptest_r2"],[ltest_r2,ptest_r2],color=["blue","green"])
plt.ylabel("r2 score")
plt.show()



######["ltest_mse","ptest_mse"]        pehle double quotes wala ayega baad me   [ltest_mse,ptest_mse]            , don't change the axis

f1=int(input("enter median income"))
f2=int(input("enter total bedrooms"))
user_input=np.array([[f1,f2]])     ####two boxes use honge   and parantheses bhi hai
user_input_poly=poly.fit_transform(user_input)
prediction=model.predict(user_input_poly)
print(prediction)    





























