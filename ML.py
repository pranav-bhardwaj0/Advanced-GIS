#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 15:40:31 2021

@author: Pranav Bhardwaj, Sebastian Dodt, Philippe Schicker
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
from sklearn.model_selection import train_test_split # Sklearn recommended as a good beginners ML library
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix



## To make our output more easily readible, we remove the warnings that are not integral to our script.
pd.options.mode.chained_assignment = None


## Importing data
df = pd.read_csv("df.csv", index_col = 3)

## dropping columns not relevant for our analysis
df.drop("Unnamed: 0", axis = 1, inplace = True)
df.drop("Avg Precipitation (1901 - 2000)", axis = 1, inplace = True)
df.drop("Avg Temp (1901 - 2000)", axis = 1, inplace = True)


## Choosing predictors for our ML model. We only use the "count" column, 
## i.e., the absolute number of forest fires in a county in one decade.
X = df[df.columns[[1, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43] + 
                  list(range(51,76,1))]]
### Our outcome variable for our training and testing is the number of forest fires from 2010 to 2019.
y = df[df.columns[46]] 

### We split the full data into training (80%) and testing (20%). 
### We set the random_state = 314 to have reproducible results.
### We also make sure that a similar number of counties fromo each state are represented in both datasets.
X_train, X_test, y_train, y_test = train_test_split(
                                        X, y,
                                        test_size = 0.2,
                                        random_state = 314,
                                        stratify = df["STATE_NAME"])
### After statifying on the state, we don't need that column anymore.
X_train.drop("STATE_NAME", axis = 1, inplace = True)
X_test.drop("STATE_NAME", axis = 1, inplace = True)


### We fit the model. After multiple iterations and a comparison of the Root Mean Squared Errors for 
### different values for "n_neighbors", we choose 8 as the optimal number of nearest neighbors. 
### While an even number such as 8 is uncommon for knn models, it's not a problem because we are not 
### fitting a classification model.
knn_model = KNeighborsRegressor(n_neighbors=8)
knn_model.fit(X_train, y_train)


### Calculating the training root-mean-squared error
predictions_on_training_data = knn_model.predict(X_train)
mse = mean_squared_error(y_train, predictions_on_training_data)
rmse = sqrt(mse)
print("The training RMSE is:",rmse)

### Calculating the testing root-mean-squared error
pred_test = knn_model.predict(X_test)
mse = mean_squared_error(y_test, pred_test)
rmse = sqrt(mse)
print("The testing RMSE is:",rmse,"\n")

### Producing a graph that shows how well our model is performing on a 
### Setting a nice colour that is also well differentiable for colour-blind people.
cmap = sns.color_palette("flare", as_cmap=True)
scale, scatterplot = plt.subplots()
points = scatterplot.scatter(y_test, pred_test, 
                    c=pred_test, s=20, cmap=cmap)
### The colorful bar is only for aesthetic purposes to illustrate the counties with more fires in a darker red. 
scale.colorbar(points)
### Setting a logarithmic scale because the data is very skewed.
scatterplot.set(xscale="log", yscale="log")
plt.xlabel("True Number of Fires per decade")
plt.ylabel("Predicted Number of Fires per decade")
plt.title("8-Nearest-Neighbor")
### Setting x-axis and y-axis limits just to make it look more squared.
scatterplot.set(ylim=(0, 11000)) 
scatterplot.set(xlim = (0, 11000))
### It complains that 0 cannot be set as a lower limit on a logarithmic scale. 
### We can ignore that warning because it still does what it is supposed to do.
plt.savefig("8nn-model_predictions.png",dpi=300)
### We save the file in a higher resolution in our working directory.
plt.show()


### Here, we create a confusion matrix to see if the model is good at classifying 
### whether or not there will be a fire in a county.
comparison = pd.DataFrame(y_test)
comparison["prediction"] = pred_test
comparison["actual_binary"] = comparison["F2010_2019_COUNT"] > 0
comparison["pred_binary"] = comparison["prediction"] > 0
print("\nConfusion matrix:\n",confusion_matrix(comparison["actual_binary"], comparison["pred_binary"]))
print("If we use our algorithm to classify counties into 'fire' and 'no fire', it is 71.4% accurate.\n")


# Future extrapolation

### Now we would like to apply the model to future data. For that we simply shift 
### the columns in our training dataset back by one decade, and add a new column with 
### simulated future data. We reuse the column titles from before so our model can identify
### the right precictors, but the column titles are technically wrong by one century.
### We keep the land data constant. 
old_col_names = X.columns
X_future = df[df.columns[[1, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 51] + 
                  list(range(53,76,1)) + [75]]]
X_future.columns = old_col_names 
X_future["Temp_2010_2019"] += 0 # Here, we add 0°C to the data (in relation to the 2010-2019 mean) 
                                # to see if the algorithm predicts the true number of the last decade.
X_future.drop("STATE_NAME", axis = 1, inplace = True)
future_pred = knn_model.predict(X_future)
print("Predicted average number of fires with 0°C increase:\n",np.mean(future_pred))
print("Actual average number of fires with 0°C increase (i.e., 2010-2019 mean):\n",np.mean(y))
### Our model is a bit too optimistic. It is somewhat biased towards predicting too little number of wildfires per county.
### We go forward with it anyway, while keeping this bias in mind.




# We fit the entire knn model again, this time with less predictors. 
# This makes each variable more important and therefore shows more significant 
# trends when we change just one of them (the temperature and precipitation for 
# the current 2020-2029 decade).
# The code is not annotated because it is identitical to the previous one.
df = pd.read_csv("df.csv", index_col = 3)
df.drop("Unnamed: 0", axis = 1, inplace = True)
df.drop("Avg Precipitation (1901 - 2000)", axis = 1, inplace = True)
df.drop("Avg Temp (1901 - 2000)", axis = 1, inplace = True)
X = df[df.columns[[1, 40, 43, 51, 61, 62, 63, 73, 74, 75]]] ## This is changed
y = df[df.columns[46]]
X_train, X_test, y_train, y_test = train_test_split(
                                        X, y,
                                        test_size = 0.2,
                                        random_state = 314,
                                        stratify = df["STATE_NAME"])
X_train.drop("STATE_NAME", axis = 1, inplace = True)
X_test.drop("STATE_NAME", axis = 1, inplace = True)
knn_model = KNeighborsRegressor(n_neighbors=8)
knn_model.fit(X_train, y_train)
old_col_names = X.columns
X_future = df[df.columns[[1, 43, 46, 51, 62, 63, 63, 74, 75, 75]]]
X_future.columns = old_col_names
X_future["Temp_2010_2019"] += 0
X_future.drop("STATE_NAME", axis = 1, inplace = True)
future_pred = knn_model.predict(X_future)


### TEMPERATURE
## Now we increase the temperature for the upcoming decade by 0.0 to 1.5°C in comparison to the 2010-2019 mean.
increase = []
mean_pred = []
median_pred = []
for i in list(range(0,50,1)):
    X_future["Temp_2010_2019"] += i/(20*1.8) ## We divide by 1.8 to convert from °F to °C. 
    future_pred = knn_model.predict(X_future)
    increase.append(i/ (20 * 1.8))
    mean_pred.append(np.mean(future_pred))
    median_pred.append(np.median(future_pred))
## Mean prediction now contains the average number of wildfires predicted respective to the increase in temperature.

sns.lineplot(increase, mean_pred, color = "red")
plt.title("Increase in predicted wildfires because of temperature change")
plt.xlabel("Increase in °C compared to 2010-2019 average")
## We choose to work with °C since that's what most use in popular science around 
## climate change and also because we are not from the US :) 
plt.ylabel("Average number of wildfires predicted\nfor 2020-2029 period per county")
plt.savefig("temp_change.png",dpi=300)
plt.show()


### PRECIPITATION
### We decrease the precipiation in every county by a certain percentage of its 2010-2019 level.
prec_decrease = []
mean_prec_pred = []
median_prec_pred = []
for i in list(range(-25, 0, 1)):
     # We choose the range [-25%, 0%] because this is the precipiation decrease that is expected in the upcoming decades.
    X_future["Prec_2010_2019"] -= X_future["Prec_2010_2019"]*(-1 * i)/100
    future_pred = knn_model.predict(X_future)
    prec_decrease.append(i)
    mean_prec_pred.append(np.mean(future_pred))
    median_prec_pred.append(np.median(future_pred))

sns.lineplot(prec_decrease, mean_prec_pred, color = "blue")
plt.title("Increase in predicted wildfires because of precipitation change")
plt.xlabel("percentage decrease in annual precipitation")
plt.ylabel("Average number of wildfires predicted\nfor 2020-2029 period per county")
plt.savefig("prec_change.png",dpi=300)
plt.show()

