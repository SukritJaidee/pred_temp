# -*- coding: utf-8 -*-
"""weather_submit_v1_04025566_1250.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hSSRyLhanIMrE4L9xIknK1uW0atAmFT_
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/SukritJaidee/pred_temp.git 
# %cd /content/pred_temp

!pip install -q meteostat
!pip install -q mercantile
!pip install -q mpmath

import pytz
import json
import warnings
import requests
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
# from pycaret.regression import *
from tqdm.notebook import tqdm
from datetime import datetime, timedelta, date, tzinfo
warnings.filterwarnings("ignore")

from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

from pred_temp.x3_ibm_api import x3_api
from pred_temp.tmd_api import tmd_weather
from pred_temp.x4_weather_api import x4_api
from pred_temp.loc_level10 import get_level10_pos
from pred_temp.x1_station_meteo_api import x1_api
from pred_temp.x2_point_meteo_api import x2_api, x1_station_x2

path_save = 'drive/MyDrive/result_weather/'
path = '/content/drive/MyDrive/chula_weather/one_model/keras_model/'
root_path =  '/content/drive/MyDrive/chula_weather/one_model/last_dataset/'

cols =  ['lat', 'lon', 'latitude', 'longitude', 'elevation', 'distance', 'temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'year', 'month', 'day', 'hour', 'minute', 'temp.1', 'dwpt.1', 'rhum.1', 'wdir.1', 'wspd.1',
                    'pres', 'lat.1', 'lon.1', 'year.1', 'month.1', 'day.1', 'hour.1', 'minute.1', 'requestedLatitude', 'requestedLongitude', 'latitude.1', 'longitude.1', 'precip1Hour', 'precip6Hour', 'precip24Hour', 'pressureChange',
                    'pressureMeanSeaLevel', 'relativeHumidity', 'temperature', 'temperatureChange24Hour', 'temperatureMax24Hour', 'temperatureMin24Hour', 'temperatureDewPoint', 'temperatureFeelsLike', 'uvIndex',
                    'visibility', 'windDirection', 'windSpeed', 'lat.2', 'lon.2', 'lats', 'lons', 'temp_cs', 'wind_kphs', 'wind_degrees', 'wind_dirs', 'pressure_mbs', 'precip_mms', 'humiditys', 'clouds', 'feelslike_cs',
                    'windchill_cs', 'heatindex_cs', 'dewpoint_cs', 'will_it_rains', 'chance_of_rains', 'vis_kms', 'gust_kphs']

df = pd.read_csv(root_path+'final_data.csv')
x, y = df.drop("temperature", axis = 1), df[["temperature"]] 
X_train, X_test, y_train, y_test = train_test_split(x, y,  test_size=0.2, shuffle=True)

def ann_model(X_train):
    layer = tf.keras.layers.experimental.preprocessing.Normalization()
    layer.adapt(X_train)
    model = keras.Sequential([layer,
      keras.layers.Dense(64, activation='relu', kernel_initializer='normal', kernel_regularizer="l2", input_shape=(68,)),
      keras.layers.Dropout(0.2),
      keras.layers.Dense(32, activation='relu', kernel_initializer='normal', kernel_regularizer="l2"),
      keras.layers.Dropout(0.2),
      keras.layers.Dense(1, activation='relu')
      ])
    loss = tf.keras.losses.MeanSquaredError(name="mse")
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
    m1 = tf.keras.metrics.RootMeanSquaredError()
    m2 = tf.keras.metrics.MeanAbsoluteError()
    model.compile( optimizer=optimizer,  loss = loss, metrics = [m1, m2])
    return model

def cal_from_source(q1, now_datetime, format_date, saved_lr):
  #### x0
  diff_time, hour, duration = 0, 0, 24
  day = (datetime.now(pytz.timezone('Asia/Bangkok'))+timedelta(diff_time)).strftime("%Y-%m-%d")
  x0 = tmd_weather(q1[0], q1[1], day, hour, duration)
  #### x1
  start_date, end_date = -1, 1
  start = pd.to_datetime((now_datetime+timedelta(start_date)).strftime(format_date)) 
  end = pd.to_datetime((now_datetime+timedelta(end_date)).strftime(format_date))
  x1 = x1_api(q1, start, end)
  #### x2
  start_date, end_date = -1, 1
  start = pd.to_datetime((now_datetime+timedelta(start_date)).strftime(format_date)) 
  end = pd.to_datetime((now_datetime+timedelta(end_date)).strftime(format_date))
  x2 = x2_api(q1, start, end)
  if x2.shape[0] == 0:
    x2 = x1_station_x2(q1, start=-1, end=0)
    x2.drop(['latitude', 'longitude', 'elevation', 'distance'], axis=1, inplace=True)
    x2 = x2.reindex(columns=['temp', 'dwpt', 'rhum', 'wdir', 'wspd', 'pres', 'lat', 'lon', 'year', 'month', 'day', 'hour', 'minute'])
  #### x3
  apikey =  "2601b3bc3f684d2681b3bc3f687d26f8"
  format_date, start_date, end_date  = "%Y-%m-%d", -1, 1
  start = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
  end = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
  x3 = x3_api(q1, start, end, apikey)
  #### x4
  format_date, start_date, end_date = "%Y-%m-%d", 0, 1
  start = pd.to_datetime(now_datetime+timedelta(start_date)).strftime(format_date)
  end = pd.to_datetime(now_datetime+timedelta(end_date)).strftime(format_date)
  x4  = x4_api(q1, start, end)
  res = pd.concat([x0, x1, x2, x3, x4], axis=1,  join="inner")
  res1 = res.drop(['tc', 'rh', 'datatime'], axis=1)
  res1.columns = cols
  temp_po = res1[['temperature']].iloc[-1:,:]
  temp_po.reset_index(drop=True, inplace=True)
  res1 = res1.drop(['temperature'], axis=1)
  one_res1 = res1.iloc[-1:,:]

  y_pred = saved_lr.predict(one_res1, verbose=0)
  y_pred = pd.DataFrame(y_pred, columns = ['ypred'])

  actual = res[['tc', 'datatime']]
  one_actual = actual.iloc[-1:,:]
  one_actual.reset_index(drop=True, inplace=True)

  res2 = pd.concat([y_pred, one_actual, temp_po], axis=1,  join="inner")
  data = res2.iloc[-1:,:]
  return data

df = get_level10_pos() 
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
format_date = "%Y-%m-%d %H:%M:%S"
models = 'keras_best_model_rmse_0528_mse_04208.h5'
lats, lons, datetimes, pred_vals, tmd_vals = [], [], [],  [], []
x_tiles, y_tiles = [], []
saved_lr = ann_model(X_train)
saved_lr.load_weights(path+models)

start_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
for  i in tqdm(range(len(df))):
# for  i in tqdm(range(1,10)):
  lat, lon = df['lat_south'][i], df['lon_east'][i]
  x_tile, y_tile = df['x_tiles'][i], df['y_tiles'][i]
  q1 = (lat, lon)
  try:
      data = cal_from_source(q1, now_datetime, format_date, saved_lr)
      pred_val, tmd = data['ypred'][0], data['tc'][0]
      x_tiles.append(x_tile); y_tiles.append(y_tile); 
      lats.append(lat); lons.append(lon); pred_vals.append(pred_val); tmd_vals.append(tmd);
  except:
      pred_val, tmd = data['temperature'][0], data['tc'][0]
      lats.append(lat); lons.append(lon);
      x_tiles.append(x_tile); y_tiles.append(y_tile); 
      pred_vals.append(pred_val); tmd_vals.append(tmd);
      print(f"Error  lat = {round(q1[0],2)} lon = {round(q1[1],2)}")

success = True
end_cp = datetime.now(pytz.timezone('Asia/Bangkok'))
delta = end_cp - start_cp
sec = delta.total_seconds()
min = sec/60
print('minutes:', min)

format_save = "%d%m%Y-%H:%M"
now_datetime  = datetime.now(pytz.timezone('Asia/Bangkok'))
save_datetime = now_datetime.strftime(format_save) 
info_data = {'success':[success], 'datetime':[save_datetime],'start_compute':[start_cp],'end_compute':[end_cp]}
df5 = pd.DataFrame({'lat':lats,'lon':lons,'x_tiles':x_tiles, 'y_tiles':y_tiles, 'blend temp':pred_vals,'TMD temp':tmd_vals,})
df6 = pd.DataFrame(info_data)
df5.to_csv('/content/'+path_save+'data/onetime/'+save_datetime+'_data.csv' ,encoding='utf-8-sig')
df6.to_csv('/content/'+path_save+'data/onetime/'+save_datetime+'_info.csv' ,encoding='utf-8-sig')

#@title Backup
# !pip install -r requirements_colab_r1.txt
# !pip install scikit-learn==1.2.0 #[1.0.1, 1.0.2, 0.23.2]
# !pip install APScheduler
# !pip install apscheduler
# !pip install --pre pycaret[full]
# !pip install git+https://github.com/pycaret/pycaret.git#egg=pycaret

  ## for pycaret
  # try:
  #   unseen_pred = predict_model(saved_lr, data=res1)
  # except:
  #   res1 = res1.astype('float32')
  #   unseen_pred = saved_lr.predict(res1)

  # models = 'Final Blend Model 20112022_950_ibm'

# saved_lr = load_model(models)
# saved_lr = tf.keras.models.load_model(path+models)

# pred_val = data['prediction_label'][0] # for pycaret

# df5['x'] = df5['lon'].apply(lambda x: (int(pow(2, 10)*(x + 180) / 360)))
# df5['y'] = df5['lat'].apply(lambda x:  int(pow(2, 10)*(1 - log(tan(radians(x)) + sec(radians(x))) / pi) / 2))