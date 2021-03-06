# -*- coding: utf-8 -*-
"""STOCK_MARKET_PREDICTION_PROJECT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/DevlinaPal/LGMVIP-DataScience/blob/main/Beginner-level/STOCK%20MARKET%20PREDICTION%20USING%20STACKEDLSTM/STOCK_MARKET_PREDICTION_PROJECT.ipynb

NAME- RAJ KAMAL SHAKYA

LGM-VIP INTERNSHIP

BEGINNER LEVEL TASK -2

Stock Market Prediction And Forecasting Using Stacked LSTM

1. IMPORT LIBRARY
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

"""2. LOAD DATA"""

data=pd.read_csv("NSE.csv")

data.head()

data.tail()

# sort with date 
data['Date']=pd.to_datetime(data['Date'])
print(type(data.Date[0]))

df=data.sort_values(by='Date')
df.head()

df.reset_index(inplace=True)

df.head()

plt.plot(df['Close'])

df1=df['Close']

"""3. PREPARE DATA"""

## LSTM are sensitive to the scale of the data,therefore applying MinMax scaler 
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
df1

##splitting dataset into train and test split
training_size=int(len(df1)*0.70)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

training_size,test_size

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return np.array(dataX), np.array(dataY)

# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)

print(X_train.shape), print(y_train.shape)

print(X_test.shape), print(ytest.shape)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

"""4. MODEL BUILDING"""

### Create the Stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.summary()

model.fit(X_train,y_train,validation_split=0.1,epochs=60,batch_size=64,verbose=1)

## Lets do the prediction and check performance metrics
test_predict=model.predict(X_test)

## Transform back to original form
test_predict1=scaler.inverse_transform(test_predict)

test_predict1

## Calculate RMSE performance metrics
import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(ytest,test_predict))