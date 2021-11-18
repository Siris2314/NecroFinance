import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt 
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout,LSTM


def predict_crypto(crypto, world, start_date, end_date, days):
   
    crypto_currency = crypto
    world_currency = world
    start = start_date
    end = end_date

    data = web.DataReader(f'{crypto_currency}-{world_currency}', 'yahoo', start, end)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

    prediction_days = days

    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)): 
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])
        
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()

    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences = True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, epochs=25, batch_size=32)



    year, month, day = map(int, start.split('-'))
    year2,month2, day2 = map(int, end.split('-'))
    test_start = dt.datetime(year,month,day)
    test_end = dt.datetime(year2,month2,day2)


    test_data =  data = web.DataReader(f'{crypto_currency}-{world_currency}', 'yahoo', test_start, test_end)
    actual_prices = test_data['Close'].values

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1,1)
    model_inputs = scaler.fit_transform(model_inputs)

    x_test = []

    for x in range(prediction_days, len(model_inputs)): 
        x_test.append(model_inputs[x-prediction_days:x,0]) 

    x_test = np.array(x_test)
    x_test = np.reshape(x_test,(x_test.shape[0], x_test.shape[1], 1)) 

    prediction_prices = model.predict(x_test) 
    prediction_prices = scaler.inverse_transform(prediction_prices) 

    return prediction_prices[0][0]











    

