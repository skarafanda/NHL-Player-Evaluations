import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
from IPython.display import display
from sklearn.linear_model import LinearRegression;
from sklearn.model_selection import train_test_split;

df = pd.read_csv('LeagueStats_2022-23.csv')
#display(df) #Really useful in Jupyter Notebook for visualizing dataset.
display(df[["fullName","points","powerPlayTimeOnIcePerGameSec"]].sort_values("points",ascending=False))

#Finding Linear Regression using train test split
X = np.array(df["powerPlayTimeOnIcePerGameSec"]).reshape((-1, 1))
y = np.array(df["points"])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

regressor = LinearRegression().fit(X_train, y_train)

y_pred = regressor.predict(X_test)


# #Interesting hexbin plot that helps view the clumps of data around the origin (although the half hexs on y-axis look odd). 
# plt.hexbin(np.array(df["powerPlayTimeOnIcePerGameSec"]), y, gridsize=(10,10), cmap=plt.cm.RdBu, vmin=0, vmax=60)
# plt.plot(X_test, y_pred, color="k")
# plt.colorbar()
# plt.xlabel("PP TOI (sec)")
# plt.ylabel("points")
# plt.show()

# #Scatterplot with the same data for comparison. 
# plt.scatter(X_train, y_train, color="green")
# plt.plot(X_test, y_pred, color="k")
# plt.xlabel("PP TOI (sec)")
# plt.ylabel("points")
# plt.show()

#Finding R Squared Value
# r_sq = regressor.score(X, y)
# print(r_sq) #0.587380759244329


#Finding Linear Regression with all of the data (no splitting)
# x = np.array(df['powerPlayTimeOnIcePerGameSec']).reshape((-1,1))
# y = np.array(df['points'])

# model = LinearRegression().fit(x, y)

# r_sq = model.score(x, y)
# print(r_sq) #0.5877954376741221